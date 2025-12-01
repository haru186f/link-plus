from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.shortcuts import render

from .models import BusStop, BusSchedule, College, Department, Course, ReceivedEmail, LectureSchedule

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

# ---------------------------------------------------
# ✨ メール一覧表示 ✨
# ---------------------------------------------------
def mail_list_view(request):
    """
    すべての受信メールを表示するためのビュー。
    """
    # データベースからすべてのメールオブジェクトを取得します
    # 通常は新しい順に並べ替えます
    all_emails = ReceivedEmail.objects.all().order_by('-received_at')

    context = {
        'all_emails': all_emails,
        'page_title': 'すべての受信メール'
    }

    # mail_list.html' という新しいテンプレートをレンダリングします
    return render(request, 'core/mail_list.html', context)

# ---------------------------------------------------
# ✨ LectureSchedule API（FullCalendar用） ✨
# ---------------------------------------------------
def lecture_events(request):
    """講義スケジュールをFullCalendar形式で返すAPI"""
    events = []

    weekday_map = ["mon", "tue", "wed", "thu", "fri"]

    for lec in LectureSchedule.objects.select_related("room", "course"):
        # FullCalendar の daysOfWeek（0=日〜 6=土）
        if lec.day_of_week in weekday_map:
            fc_day = weekday_map.index(lec.day_of_week) + 1  # 月=1 → FC

        events.append({
            "title": lec.name,
            "daysOfWeek": [fc_day],   # 毎週表示に必要
            "startTime": lec.start_time.strftime("%H:%M"),
            "endTime": lec.end_time.strftime("%H:%M"),
            "extendedProps": {
                "room": lec.room.name,
                "course": lec.course.name,
                "period": f"{lec.start_period}〜{lec.end_period}限",
                "is_canceled": lec.is_canceled
            }
        })

    return JsonResponse(events, safe=False)
