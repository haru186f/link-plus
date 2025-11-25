import datetime

from apps.core.models import BusSchedule, BusStop


def calc_remaining(self, target_time):
    """現在時刻との差分(分)を返す。翌日も考慮。"""
    now = datetime.now()
    target = datetime.combine(now.date(), target_time)

    # 翌日対応
    if target < now:
        target += datetime.timedelta(days=1)

    diff = (target - now).total_seconds() / 60
    return round(diff)

def get_bus_data(self):
    """バス情報を整形して返す"""

    now = datetime.now().time()
    bus_data = {}

    # 全スケジュールを先に取得（効率化）
    schedules = BusSchedule.objects.select_related('bus_stop').order_by('station_departure', 'campus_departure')

    for bus in BusStop.objects.all():
        bus_schedules = [s for s in schedules if s.bus_stop_id == bus.id]

        # 次の「駅 → 学校」便
        next_departure = next(
            (s for s in bus_schedules if s.station_departure and s.station_departure > now),
            None
        )

        # 次の「学校 → 駅」便
        next_return = next(
            (s for s in bus_schedules if s.campus_departure and s.campus_departure > now),
            None
        )

        # departure
        if next_departure:
            minutes = self.calc_remaining(next_departure.station_departure)
            dep_display = f"残り {minutes} 分"
        else:
            note = next((s.note for s in bus_schedules if s.station_departure is None and s.note), "-")
            dep_display = note

        # return
        if next_return:
            minutes = self.calc_remaining(next_return.campus_departure)
            ret_display = f"残り {minutes} 分"
        else:
            note = next((s.note for s in bus_schedules if s.campus_departure is None and s.note), "-")
            ret_display = note

        bus_data[bus.name] = {
            "departure": dep_display,
            "return": ret_display,
        }

    return bus_data
