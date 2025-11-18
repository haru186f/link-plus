from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.shortcuts import render

from .models import BusStop, BusSchedule, College, Department, Course, ReceivedEmail


# ==========================================================
# ホームビュー（全てのデータを集約）
# ==========================================================

class HomeView(TemplateView):
    template_name = 'core/home.html'

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
        schedules = BusSchedule.objects.select_related('bus').order_by('station_departure', 'campus_departure')

        for bus in BusStop.objects.all():
            bus_schedules = [s for s in schedules if s.bus_id == bus.id]

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
        context["received_emails"] = ReceivedEmail.objects.order_by('-id')[:5]

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
    if request.method != 'POST':
        return JsonResponse({'status': 'method not allowed'}, status=405)

    # JSON も form も対応
    try:
        import json
        payload = json.loads(request.body)
    except:
        payload = request.POST

    subject = payload.get('subject', 'No Subject')
    sender = payload.get('sender', 'noreply@webhook.com')
    body = payload.get('text_body', 'Empty Body')

    try:
        ReceivedEmail.objects.create(
            subject=subject,
            sender=sender,
            body=body
        )
        return JsonResponse({'status': 'success'}, status=200)
    except Exception as e:
        print(f"Error saving email: {e}")
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)
