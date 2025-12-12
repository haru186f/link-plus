from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from datetime import datetime, timedelta
from django.shortcuts import render
from django.core import serializers
import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Q # 複雑なクエリのためにQオブジェクトをインポート
from .models import LectureSchedule

from apps.core.models import College, Department, Course, BusSchedule, BusStop, ReceivedEmail, LectureSchedule

import json
import logging
logger = logging.getLogger(__name__)

# ==========================================================
# ホームビュー（全てのデータを集約）
# ==========================================================

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        """データをcontextに集約してホームページに送信する"""
        context = super().get_context_data(**kwargs)

        # contextにデータを集約
        context["bus_schedules"] = BusSchedule.objects.all()
        context["received_mails"] = ReceivedEmail.objects.all().order_by('-received_at')[:5]
        context["lecture_schedules"] = LectureSchedule.objects.all()

        return context



# ==========================================================
# ニュースビュー（お知らせのリストを返す）
# ==========================================================
class NewsListView(ListView):
    model = ReceivedEmail
    template_name = 'core/news.html'
    context_object_name = 'all_emails'
    ordering = ['-received_at']  # 新しい順

    extra_context = {
        'page_title': 'すべての受信メール'
    }

def get_data_for_modal(request):
    """
    データベースからデータを取得し、JSONで返すビュー
    """
    if request.method == 'GET':
        # データベースから全データを取得
        queryset = BusSchedule.objects.all()

        # データをJSON形式にシリアライズ
        # fields=['field1', 'field2', ...] で必要なフィールドのみ指定可能
        data = serializers.serialize('json', queryset)

        # JsonResponseでクライアントに返す
        return JsonResponse(json.loads(data), safe=False)

    # GETリクエスト以外の場合は許可しない
    return JsonResponse({'error': 'Method not allowed'}, status=405)



# ==========================================================
# エンドポイント
# ==========================================================
class GetDepartmentsView(View):
    """選択された学部に応じて学科リストを返す"""
    def get(self, request, *args, **kwargs):
        college_id = request.GET.get('college_id')
        departments = Department.objects.filter(college_id=college_id).values('id', 'name')
        return JsonResponse(list(departments), safe=False)


class GetCoursesView(View):
    """選択された学科に応じてコースリストを返す"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')
        courses = Course.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse(list(courses), safe=False)


class GetGradesView(View):
    """学科ごとに年制を返す（2年制 / 3年制 / 4年制）"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')

        # 特定の学科で分岐（3年制、4年制度）
        THREE_YEAR_DEPARTMENTS = [
            # デザインカレッジ
            'ゲームクリエイター科（3年制）',
            'デザイン科（3年制）',
            'CG映像科（3年制）',

            # スポーツ・医療カレッジ
            'スポーツトレーナー科（3年制）',
            'スポーツ健康学科（3年制）',
            '鍼灸科（3年制）',
            '柔道整復科（3年制）',
        ]
        FOUR_YEAR_DEPARTMENTS = [
            # クリエイターズカレッジ
            'マンガ・アニメーション科（4年制）',

            # デザインカレッジ
            'ゲームクリエイター科（4年制）',

            # ITカレッジ
            'ITスペシャリスト科（4年制）',

            # テクノロジーカレッジ
            '建築学科（4年制）',
            '一級自動車整備科（4年制）',
            ]

        try:
            department = Department.objects.get(id=department_id)
            if department.name in FOUR_YEAR_DEPARTMENTS:
                max_grade = 4
            elif department.name in THREE_YEAR_DEPARTMENTS:
                max_grade = 3
            else:
                max_grade = 2
        except Department.DoesNotExist:
            max_grade = 2

        return JsonResponse({'max_grade': max_grade})


def receive_email_webhook(request):
    if request.method == 'POST':
        # 外部からのリクエストデータから情報を取得（例：Webhookペイロード）
        email_data = request.POST

        try:
            # 💡 ここでデータ保存ロジックを実行しています 💡
            ReceivedEmail.objects.create(
                # request.POSTから抽出した値を使ってDBに保存
                subject=email_data.get('subject', 'No Subject'),
                sender=email_data.get('sender', 'noreply@webhook.com'),
                body=email_data.get('text_body', 'Empty Body')
            )
            return JsonResponse({'status': 'success'}, status=200)

        except Exception as e:
            # データベースエラーなどが発生した場合の応答
            print(f"Error saving email: {e}")
            return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)

    # POSTメソッド以外でアクセスされた場合の応答
    return JsonResponse({'status': 'method not allowed'}, status=405)


def api_email_body(request, pk):
    """
    指定された主キー(pk)のメール本文と件名をJSONで返すAPIエンドポイント。
    home.htmlのAJAXリクエストから呼び出されます。
    """
    if request.method == 'GET':
        try:
            # 1. PKに基づいてメールを取得
            email = ReceivedEmail.objects.get(pk=pk)

            # 2. データをJSON形式で整形
            data = {
                'subject': email.subject,
                'body': email.body,
            }

            # 3. JSONレスポンスを返す
            return JsonResponse(data)

        except ReceivedEmail.DoesNotExist:
            # 指定されたIDのメールが見つからない場合
            return JsonResponse({'error': 'Email not found'}, status=404)

        except Exception as e:
            # その他のエラーが発生した場合
            logger.error(f"Error fetching email body for PK {pk}: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

    # GETメソッド以外でのリクエストを拒否
    return JsonResponse({'error': 'Method not allowed'}, status=405)


class GetNextBusInfo(View):
    """次のバス情報をJSONで返すAPI（完全版）"""

    def get(self, request, *args, **kwargs):

        def calc_remaining_minutes(target_time):
            """次の出発時刻までの残り分数。
            ・0分 → 表示する
            ・-1分以下 → スキップして None を返す
            """
            now = datetime.datetime.now()
            target = datetime.datetime.combine(now.date(), target_time)

            diff = (target - now).total_seconds() / 60

            if diff < 0:
                return None  # ★ -1分以下は無視（次の便へ）

            remain = round(diff)

            return remain  # ★ 0分はそのまま返す

        now = datetime.datetime.now().time()
        result = {}

        schedules = BusSchedule.objects.select_related('bus_stop').order_by(
            'station_departure',
            'campus_departure'
        )

        for bus_stop in BusStop.objects.all():
            stop_schedules = [s for s in schedules if s.bus_stop == bus_stop]

            # --- 駅 → キャンパス ---
            next_departure = None
            for s in stop_schedules:
                if s.station_departure:
                    remain = calc_remaining_minutes(s.station_departure)
                    if remain is not None:  # -1や過ぎた便は除外、0分は表示
                        next_departure = remain
                        break

            # --- キャンパス → 駅 ---
            next_return = None
            for s in stop_schedules:
                if s.campus_departure:
                    remain = calc_remaining_minutes(s.campus_departure)
                    if remain is not None:
                        next_return = remain
                        break

            # --- note fallback ---
            if next_departure is None:
                next_departure = next((s.note for s in stop_schedules if s.note), "-")

            if next_return is None:
                next_return = next((s.note for s in stop_schedules if s.note), "-")

            result[bus_stop.name] = {
                "label": bus_stop.get_name_display(),  # type: ignore
                "departure_to_campus": next_departure,
                "return_to_station": next_return,
            }

        return JsonResponse(result)


class DebugBusSchedule(View):
    def get(self, request, *args, **kwargs):
        data = []

        for s in BusSchedule.objects.select_related("bus_stop").order_by(
            "bus_stop__name", "station_departure", "campus_departure"
        ):
            data.append({
                "bus_stop": s.bus_stop.name,
                "station_departure": s.station_departure.strftime("%H:%M") if s.station_departure else None,
                "campus_departure": s.campus_departure.strftime("%H:%M") if s.campus_departure else None,
                "note": s.note,
            })

        return JsonResponse(data, safe=False)


# ==========================================================
#   FullCalendarAPI
# ==========================================================
def lecture_events(request):
    """講義スケジュールをFullCalendar形式で返すAPI"""

    try:
        # 認証済みのユーザーのプロフィールを取得
        user_profile = request.user.profile
    except Exception:
        # プロフィールがない、または認証されていない場合
        return JsonResponse([], safe=False)

    # ユーザーの所属情報を取得
    target_department = user_profile.department
    target_course = user_profile.course  # コースがない場合は None になる
    target_grade = user_profile.grade
    target_class_number = user_profile.class_number

    # フィルタリング条件を構築
    # 講義は、以下の条件すべてを満たす必要がある：
    # 1. 学科が一致する
    # 2. 学年が一致する
    # 3. クラスが一致する
    base_filter = Q(
        department=target_department,
        target_grade=target_grade,
        target_class_number=target_class_number,
    )

    if target_course:
        # プロフィールにコースが設定されている場合
        # → そのコースに紐づいた講義のみを対象とする
        final_filter = base_filter & Q(course=target_course)
    else:
        # プロフィールにコースが設定されていない場合 (コースがない学科)
        # → コースが NULL である講義のみを対象とする
        final_filter = base_filter & Q(course__isnull=True)

    # 絞り込まれた講義スケジュールを取得
    lectures = LectureSchedule.objects.select_related("room", "department", "course").filter(final_filter)

    events = []
    weekday_map = ["mon", "tue", "wed", "thu", "fri"]

    for lec in lectures:
        if lec.day_of_week in weekday_map:
             fc_day = weekday_map.index(lec.day_of_week) + 1

        events.append({
            "title": lec.name,
            "daysOfWeek": [fc_day],
            "startTime": lec.start_time.strftime("%H:%M"),
            "endTime": lec.end_time.strftime("%H:%M"),
            "extendedProps": {
                "room": lec.room.name,
                "department": lec.department.name, # 表示用に学科名を追加
                "course": lec.course.name if lec.course else "―", # コース名を表示
                "period": f"{lec.start_period}〜{lec.end_period}限",
                "is_canceled": lec.is_canceled
            }
        })

    return JsonResponse(events, safe=False)
