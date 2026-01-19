from .models import BusStop, BusSchedule
import math
from django.views import View
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.urls import reverse_lazy
from django.shortcuts import redirect
import datetime
from django.db.models import Q  # 複雑なクエリのためにQオブジェクトをインポート
from .models import LectureSchedule
from .forms import AnnouncementForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

from apps.core.models import College, Department, Course, BusSchedule, BusStop, ReceivedEmail, LectureSchedule, Event
from apps.core.forms import LectureScheduleForm, EventForm

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

        user_dept = None
        user_grade = None
        if self.request.user.is_authenticated:
            try:
                user_dept = self.request.user.profile.department
                user_grade = self.request.user.profile.grade
            except:
                pass

        # contextにデータを集約
        context["bus_schedules"] = BusSchedule.objects.all()
        context["received_mails"] = ReceivedEmail.objects.filter(
            (Q(target_department=user_dept) | Q(target_department__isnull=True)) &
            (Q(target_grade=user_grade) | Q(target_grade__isnull=True))
        ).order_by('-received_at')[:5]
        context["lecture_schedules"] = LectureSchedule.objects.all()

        return context


def home(request):
    if request.user.is_authenticated:
        # ログインしている人は全部見える
        events = Event.objects.all()
    else:
        # ログインしていない人は、プルダウンで「すべて(True)」にしたものだけ見える
        events = Event.objects.filter(is_external=True)

    return render(request, 'core/home.html', {'events': events})


# ==========================================================
# ニュースビュー（お知らせのリストを返す）
# ==========================================================
class NewsListView(ListView):
    model = ReceivedEmail
    template_name = 'core/news.html'
    context_object_name = 'all_emails'

    def get_queryset(self):
        user_dept = None
        if self.request.user.is_authenticated:
            try:
                user_dept = self.request.user.profile.department
                user_grade = self.request.user.profile.grade
            except:
                pass

        return ReceivedEmail.objects.filter(
            (Q(target_department=user_dept) | Q(target_department__isnull=True)) &
            (Q(target_grade=user_grade) | Q(target_grade__isnull=True))
        ).order_by('-received_at')

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
# ニュース投稿（お知らせのリストを返す）
# ==========================================================


@user_passes_test(lambda u: u.is_teacher)
def announcement_create(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            # commit=False で一旦インスタンスを作り、足りない情報を補填する
            announcement = form.save(commit=False)
            announcement.sender = request.user.email
            announcement.received_at = timezone.now()
            announcement.message_uid = f"manual-{timezone.now().timestamp()}"
            announcement.save()  # ここで学科も含めて保存される
            # ---------------------------------------
            return redirect('core:home')
    else:
        form = AnnouncementForm()

    return render(request, 'core/announcement_form.html', {'form': form})
# 時間割ビュー
# ==========================================================


class TeacherRequiredMixin(UserPassesTestMixin):
    """
    is_teacher=Trueのユーザーのみにアクセスを許可するMixin
    （未認証または権限がない場合は、ホーム画面へリダイレクト）
    """
    # 権限がない場合はホーム画面へリダイレクト
    permission_denied_url = reverse_lazy("core:home")

    def test_func(self):
        # 認証済み かつ is_teacher=True であるかを確認
        user = self.request.user
        return user.is_authenticated and getattr(user, 'is_teacher', False)


class LectureScheduleListView(
    TeacherRequiredMixin,
    ListView,
):
    """
    教員による時間割一覧表示ビュー（Read）
    （全時間割を取得し、曜日ごとにグループ化して表示する）
    """
    template_name = "timetable/lecture_schedule_list.html"
    model = LectureSchedule

    def get_queryset(self):
        """時間割データを取得し、事前にロード(selected_related)する"""
        user_profile = self.request.user.profile

        # 1. 基本フィルタ（学科・学年・クラス）
        # ※もし管理職など「全学科見たい」場合はここを if 分岐させます
        queryset = self.model.objects.select_related(
            "start_period", "end_period", "department", "course", "room"
        ).filter(
            department=user_profile.department,
            target_grade=user_profile.grade,
            target_class_number=user_profile.class_number,
        )

        # 2. コース（専攻）の判定
        if user_profile.course:
            queryset = queryset.filter(course=user_profile.course)
        else:
            queryset = queryset.filter(course__isnull=True)

        # 3. 並び替え（曜日順 ＞ 時限順）
        return queryset.order_by("weekday", "start_period__period")

    def get_context_data(self, **kwargs):
        """時間割データを曜日ごとにグループ化し、テンプレートに渡す"""
        context = super().get_context_data(**kwargs)

        schedules = self.object_list
        weekdays = LectureSchedule.Weekday.choices

        # 曜日ごとにグループ化
        grouped = {v: [] for v, _ in weekdays}
        for schedule in schedules:
            grouped[schedule.weekday].append(schedule)

        # テンプレートに渡すためのリスト構造に整形（曜日の並びを保持）
        context["grouped_schedules"] = [
            {
                "value": value,
                "label": label,
                "schedules": grouped[value],
            }
            for value, label in weekdays
        ]
        return context


class LectureScheduleCreateView(
    TeacherRequiredMixin,
    SuccessMessageMixin,
    CreateView
):
    """
    教師による時間割作成ビュー（Create）
    （URLパラメータから曜日を初期値として設定する）
    """
    model = LectureSchedule
    form_class = LectureScheduleForm
    template_name = "timetable/lecture_schedule_form.html"
    success_url = reverse_lazy("core:lecture_schedule_list")
    success_message = "新しい時間割を作成しました。"

    def form_valid(self, form):
        # 1. まだDBに保存せず、メモリ上にインスタンスを作る
        schedule = form.save(commit=False)

        # 2. ログインユーザー（教師）のプロフィールから情報を取得
        # teacher.profile の構造に合わせて適宜調整してください
        user_profile = self.request.user.profile

        # 3. 足りない項目を自動で埋める
        schedule.department = user_profile.department
        schedule.target_grade = user_profile.grade
        schedule.target_class_number = user_profile.class_number
        schedule.course = user_profile.course

        try:
            schedule.full_clean()
        except ValidationError as e:
            # もし重複エラーが起きたら、エラー内容をフォームに渡して入力画面に戻る
            for field, messages in e.message_dict.items():
                for message in messages:
                    form.add_error(field, message)
            return self.form_invalid(form)

        # 4. これで models.py の full_clean() をパスできるようになります
        return super().form_valid(form)

    def get_initial(self):
        """URLパラメータからweekdayを取得し、フォームの初期値として設定"""
        initial = super().get_initial()
        weekday = self.request.GET.get("weekday")
        if weekday:
            initial["weekday"] = weekday
        return initial


class LectureScheduleUpdateView(
    TeacherRequiredMixin,
    SuccessMessageMixin,
    UpdateView
):
    """
    教員による時間割更新ビュー（Update）
    """
    model = LectureSchedule
    form_class = LectureScheduleForm
    template_name = "timetable/lecture_schedule_form.html"
    success_url = reverse_lazy("core:lecture_schedule_list")
    success_message = "時間割を更新しました。"


class LectureScheduleDeleteView(
    TeacherRequiredMixin,
    SuccessMessageMixin,
    DeleteView
):
    """
    教員による時間割削除ビュー（Delete）
    （delete()をオーバーライドしてメッセージを送信）
    """
    model = LectureSchedule
    template_name = "timetable/lecture_schedule_confirm_delete.html"
    success_url = reverse_lazy("core:lecture_schedule_list")

    def delete(self, request, *args, **kwargs):
        """オブジェクト削除後、成功メッセージを送信する"""
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "時間割を削除しました。")
        return response

# ==========================================================
# エンドポイント
# ==========================================================


class GetDepartmentsView(View):
    """選択された学部に応じて学科リストを返す"""

    def get(self, request, *args, **kwargs):
        college_id = request.GET.get('college_id')
        departments = Department.objects.filter(
            college_id=college_id).values('id', 'name')
        return JsonResponse(list(departments), safe=False)


class GetCoursesView(View):
    """選択された学科に応じてコースリストを返す"""

    def get(self, request, *args, **kwargs):
        department_id = request.GET.get('department_id')
        courses = Course.objects.filter(
            department_id=department_id).values('id', 'name')
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
    def get(self, request, *args, **kwargs):

        def calc_remaining_minutes(target_time):
            # 1. そもそも時刻データがなければ即座にNone
            if target_time is None:
                print("[Debug] -> None判定されました")
                return None

            # 2. combineのミスを防ぐため、日付を跨ぐ判定を入れる
            target = datetime.datetime.combine(now.date(), target_time)
            diff_seconds = (target - now).total_seconds()
            diff_minutes = diff_seconds / 60

            # 3. 過去の時刻（-1分以下）ならNone
            if diff_minutes < -1:
                return None

            # 4. 「間もなく出発」問題を回避するため、0〜1分未満はすべて「1」にするか
            #    数値として確実に正の値を返す
            remain = round(diff_minutes)

            # もし計算結果がマイナス（直近の過去）なら、0分とする
            if remain < 0:
                remain = 0

            return remain

        target_bus_stop_name = request.GET.get('bus_stop', '八王子').strip()
        result = {}

        try:
            target_bus_stop = BusStop.objects.get(name=target_bus_stop_name)
        except BusStop.DoesNotExist:
            return JsonResponse(result, safe=False)

        # --- 【曜日判定】 ---
        now = datetime.datetime.now()  # 本番用
        # now = datetime.datetime(2025, 12, 21, 7, 0, 0) # テスト用（20日は土曜）

        # 0=月, 1=火, 2=水, 3=木, 4=金, 5=土, 6=日
        current_weekday = now.weekday()

        if current_weekday == 5:
            # 土曜日の場合：is_saturday=True のデータだけを取得
            stop_schedules = BusSchedule.objects.filter(
                bus_stop=target_bus_stop,
                is_saturday=True
            )
        elif current_weekday == 6:
            # 日曜日の場合：(もしデータがないなら) 空のクエリセット、または備考のみ
            stop_schedules = BusSchedule.objects.none()
        else:
            # 平日（月〜金）の場合：is_saturday=False のデータだけを取得
            stop_schedules = BusSchedule.objects.filter(
                bus_stop=target_bus_stop,
                is_saturday=False
            )

        # --- 駅 → キャンパス ---
        next_departure = None
        valid_departure_times = [
            s.station_departure for s in stop_schedules if s.station_departure]

        for t in sorted(valid_departure_times):
            remain = calc_remaining_minutes(t)
            if remain is not None:
                # 平日の場合のみ、30分以上空いたら備考へ逃がす
                # 土曜日は無制限に数値（残り時間）を表示する
                if current_weekday != 5 and remain > 20:
                    next_departure = None
                else:
                    next_departure = remain
                break

        # --- キャンパス → 駅 ---
        next_return = None
        valid_return_times = [
            s.campus_departure for s in stop_schedules if s.campus_departure]

        for t in sorted(valid_return_times):
            remain = calc_remaining_minutes(t)
            if remain is not None:
                # 同じく土曜日は30分制限を無視する
                if current_weekday != 5 and remain > 20:
                    next_return = None
                else:
                    next_return = remain
                break

        # 5. 【重要】数値の0さえも見つからなかった場合のみ備考を出す
        if next_departure is None:
            # 備考を探す
            note = next((s.note for s in stop_schedules if s.note), "-")
            next_departure = note

        if next_return is None:
            note = next((s.note for s in stop_schedules if s.note), "-")
            next_return = note

        result[target_bus_stop.name] = {
            "label": target_bus_stop.get_name_display(),
            "departure_to_campus": next_departure,
            "return_to_station": next_return,
        }

        return JsonResponse(result, safe=False)


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
    try:
        user_profile = request.user.profile
    except Exception:
        return JsonResponse([], safe=False)

    base_filter = Q(
        department=user_profile.department,
        target_grade=user_profile.grade,
        target_class_number=user_profile.class_number,
    )

    if user_profile.course:
        final_filter = base_filter & Q(course=user_profile.course)
    else:
        final_filter = base_filter & Q(course__isnull=True)

    lectures = LectureSchedule.objects.select_related(
        "start_period", "end_period", "room"
    ).filter(final_filter)

    events = []

    for lec in lectures:
        start_time = (
            lec.start_period.start_time.strftime("%H:%M")
            if hasattr(lec.start_period.start_time, "strftime")
            else lec.start_period.start_time[:5]
        )

        end_time = (
            lec.end_period.end_time.strftime("%H:%M")
            if hasattr(lec.end_period.end_time, "strftime")
            else lec.end_period.end_time[:5]
        )

        events.append({
            "title": lec.subject,
            "daysOfWeek": [lec.weekday + 1],  # FullCalendar仕様
            "startTime": start_time,
            "endTime": end_time,
            "extendedProps": {
                "period": lec.start_period.period,
                "room": lec.room.name if lec.room else "未定",
                "status": lec.status,
                "note": lec.note,
            },
        })

    return JsonResponse(events, safe=False)



@login_required
def internal_events_api(request):
    """
    学内イベント（ログインユーザーの学科・学年に応じて）
    """
    profile = request.user.profile

    qs = Event.objects.filter(
        is_external=False
    ).filter(
        Q(target_department__isnull=True) | Q(
            target_department=profile.department),
        Q(target_grade__isnull=True) | Q(target_grade=profile.grade),
    )

    events = [
        {
            "title": e.title,
            "start": e.start_date.isoformat(),
            "end": (e.end_date + timedelta(days=1)).isoformat(),
            "allDay": True,
            "extendedProps": {
                "description": e.description,
                "scope": "internal",
            },
        }
        for e in qs
    ]

    return JsonResponse(events, safe=False)


def external_events_api(request):
    """
    学外向けイベント（全員に公開）
    """
    qs = Event.objects.filter(is_external=True)

    events = [
        {
            "title": e.title,
            "start": e.start_date.isoformat(),
            "end": (e.end_date + timedelta(days=1)).isoformat(),
            "allDay": True,
            "extendedProps": {
                "description": e.description,
                "scope": "external",
            },
        }
        for e in qs
    ]

    return JsonResponse(events, safe=False)


class BaseEventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "core/event_form.html"
    success_url = reverse_lazy("core:home")

    is_external_value = None  # 子クラスで指定

    def form_valid(self, form):
        event = form.save(commit=False)
        event.is_external = self.is_external_value
        event.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scope"] = "external" if self.is_external_value else "internal"
        return context


class InternalEventCreateView(BaseEventCreateView):
    """
    学内イベント作成
    """
    is_external_value = False


class ExternalEventCreateView(UserPassesTestMixin, BaseEventCreateView):
    """
    学外イベント作成（管理者専用）
    """
    is_external_value = True

    def test_func(self):
        return self.request.user.is_staff
