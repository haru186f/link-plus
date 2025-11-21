from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.shortcuts import render

from .models import BusStop, BusSchedule, College, Department, Course, ReceivedEmail

import logging
logger = logging.getLogger(__name__)

# ==========================================================
# ホームビュー（全てのデータを集約）
# ==========================================================

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def calc_remaining(self, target_time):
        """現在時刻との差分(分)を返す。翌日も考慮。"""
        now = datetime.now()
        target = datetime.combine(now.date(), target_time)

        # 翌日対応
        if target < now:
            target += timedelta(days=1)

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

    def get_context_data(self, **kwargs):
        """データをcontextに集約してホームページに送信する"""
        context = super().get_context_data(**kwargs)

        # contextに全てのデータを集約
        context["bus_data"] = self.get_bus_data()
        context["received_emails"] = ReceivedEmail.objects.all().order_by('-received_at')[:5]
        return context


# ==========================================================
# API エンドポイント
# ==========================================================

class GetDepartmentsView(View):
    """学部に属する学科名を返す"""
    def get(self, request, *args, **kwargs):
        college_id = request.GET.get('college_id')
        departments = Department.objects.filter(college_id=college_id).values('id', 'name')
        return JsonResponse(list(departments), safe=False)


class GetCoursesView(View):
    """学科に属するコース名を返す"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')
        courses = Course.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse(list(courses), safe=False)


class GetGradesView(View):
    """学科ごとの修業年限を返す（モデルの 'years' を参照）"""
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')

        try:
            department = Department.objects.get(id=department_id)
            max_grade = department.years  # ★ 改善ポイント（モデル依存）
        except Department.DoesNotExist:
            max_grade = 2

        return JsonResponse({'max_grade': max_grade})


# ==========================================================
# Webhook: 受信メール保存
# ==========================================================

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


# ---------------------------------------------------
# ✨ API ビュー ✨
# ---------------------------------------------------
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
