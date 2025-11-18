from django.http import JsonResponse
from django.shortcuts import render
from .models import BusStop, BusSchedule
from datetime import datetime
from pprint import pprint

def next_bus_times(request):
    """
    八王子・八王子みなみ野の
    出発・下校それぞれ直近1本の残り時間 or note を返すビュー
    """

    now = datetime.now().time()
    bus_data = {}

    def calc_remaining(target_time):
        """現在時刻との差を分単位で計算"""
        now_dt = datetime.combine(datetime.today(), now)
        target_dt = datetime.combine(datetime.today(), target_time)
        diff = (target_dt - now_dt).total_seconds() / 60
        return round(diff) if diff >= 0 else None

    for bus in BusStop.objects.all():
        # 出発（station_departure）
        next_departure = (
            BusSchedule.objects
            .filter(bus=bus, station_departure__gt=now)
            .order_by('station_departure')
            .first()
        )
        # 下校（campus_departure）
        next_return = (
            BusSchedule.objects
            .filter(bus=bus, campus_departure__gt=now)
            .order_by('campus_departure')
            .first()
        )

        # 出発データ処理
        if next_departure and next_departure.station_departure:
            dep_remaining = calc_remaining(next_departure.station_departure)
            dep_display = f"残り {dep_remaining} 分"
        else:
            # 時刻がない場合 note を優先
            note_obj = (
                BusSchedule.objects
                .filter(bus=bus, station_departure__isnull=True)
                .exclude(note__isnull=True)
                .first()
            )
            dep_display = note_obj.note if note_obj else "-"

        # 下校データ処理
        if next_return and next_return.campus_departure:
            ret_remaining = calc_remaining(next_return.campus_departure)
            ret_display = f"残り {ret_remaining} 分"
        else:
            note_obj = (
                BusSchedule.objects
                .filter(bus=bus, campus_departure__isnull=True)
                .exclude(note__isnull=True)
                .first()
            )
            ret_display = note_obj.note if note_obj else "-"

        # 結果を格納
        bus_data[bus.name] = {
            "departure": dep_display,
            "return": ret_display,
        }

    # JSONで返す（JSによるリアルタイム更新用）
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse(bus_data)

    # デバッグ出力
    print("==== DEBUG: bus_data ====")
    pprint(bus_data)

    # HTMLに渡す
    return render(request, 'tmp.html', {'bus_data': bus_data})
