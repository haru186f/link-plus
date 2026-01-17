from django.db import models

from apps.accounts.models import Profile
from django.conf import settings
from django.core.exceptions import ValidationError

# ==========================================================
# バスモデル
# ==========================================================

# バス停


class BusStop(models.Model):
    BUS_CHOICES = [('hachiouji', '八王子'), ('minamino', '八王子みなみ野')]

    name = models.CharField(
        max_length=20, choices=BUS_CHOICES, default='hachiouji')    # バス停の名前

    def __str__(self):
        return self.name


# バスの時刻表
class BusSchedule(models.Model):
    campus_departure = models.TimeField(blank=True, null=True)     # キャンパス発（下校）
    campus_arrival = models.TimeField(blank=True, null=True)       # キャンパス着
    station_departure = models.TimeField(blank=True, null=True)    # 駅発（登校）
    note = models.CharField(max_length=100, blank=True, null=True)
    is_saturday = models.BooleanField(default=False)

    bus_stop = models.ForeignKey(
        BusStop,
        on_delete=models.CASCADE,
        related_name="bus_schedules"
    )

    def __str__(self):
        # 時刻と方向の決定
        if self.station_departure:
            direction = "登校（駅 → キャンパス）"
            time = self.station_departure
        elif self.campus_departure:
            direction = "下校（キャンパス → 駅）"
            time = self.campus_departure
        else:
            direction = "未設定"
            time = None

        # 時刻の文字列化
        time_str = time.strftime("%H:%M") if time else "----"

        day_type = "土曜" if self.is_saturday else "平日"

        return f"{self.bus_stop}・{day_type}・{direction}：{time_str}"


# ==========================================================
# 講義モデル
# ==========================================================

# カレッジ
class College(models.Model):
    name = models.CharField(max_length=100)     # カレッジ名

    def __str__(self):
        return self.name


# 学科
class Department(models.Model):
    name = models.CharField(max_length=100)             # 学科名
    max_grade = models.PositiveIntegerField(default=4)  # 最大学年（デフォルトは４年）

    # 外部キー
    college = models.ForeignKey(    # カレッジ
        College,
        on_delete=models.CASCADE,
        related_name='departments'
    )

    def __str__(self):
        return self.name


# コース
class Course(models.Model):
    name = models.CharField(max_length=100)

    # 外部キー
    department = models.ForeignKey(     # 学科
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )

    def __str__(self):
        return self.name


# ==========================================================
# 時間割モデル
# ==========================================================

# 教室
class Room(models.Model):
    name = models.CharField("教室名", max_length=100, unique=True)

    def __str__(self):
        return self.name


# 時限マスタ
class SchoolPeriod(models.Model):
    period = models.PositiveIntegerField("時限", unique=True)
    start_time = models.TimeField("開始時刻")
    end_time = models.TimeField("終了時刻")

    class Meta:
        ordering = ["period"]
        verbose_name = "時限"
        verbose_name_plural = "時限"

    def __str__(self):
        return f"{self.period}限（{self.start_time:%H:%M}-{self.end_time:%H:%M}）"


# 講義スケジュール
class LectureSchedule(models.Model):

    class Weekday(models.IntegerChoices):
        MONDAY = 0, "月曜日"
        TUESDAY = 1, "火曜日"
        WEDNESDAY = 2, "水曜日"
        THURSDAY = 3, "木曜日"
        FRIDAY = 4, "金曜日"

    class Status(models.IntegerChoices):
        NORMAL = 0, "通常"
        CANCELED = 1, "休講"
        MAKEUP = 2, "補講"

    weekday = models.PositiveSmallIntegerField("曜日", choices=Weekday.choices)
    subject = models.CharField("科目名", max_length=100)
    note = models.TextField("備考", blank=True)
    status = models.PositiveSmallIntegerField(
        "講義状態", choices=Status.choices, default=Status.NORMAL,)
    teacher = models.CharField("担当教員", null=True, blank=True,)

    target_grade = models.PositiveSmallIntegerField(
        "対象学年",
        choices=Profile.GRADE_CHOICES,
    )

    target_class_number = models.PositiveSmallIntegerField(
        "対象クラス",
        choices=Profile.CLASS_CHOICES,
    )

    # 外部キー
    start_period = models.ForeignKey(
        SchoolPeriod,
        on_delete=models.PROTECT,
        related_name="lecture_start_set",
        verbose_name="開始時限",
    )

    end_period = models.ForeignKey(
        SchoolPeriod,
        on_delete=models.PROTECT,
        related_name="lecture_end_set",
        verbose_name="終了時限",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="lecture_schedules",
        verbose_name="学科",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lecture_schedules",
        null=True,
        blank=True,
        verbose_name="コース/専攻",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name="lecture_schedules",
        null=True,
        blank=True,
        verbose_name="教室",
    )

    class Meta:
        ordering = ["weekday", "start_period__period"]
        verbose_name = "時間割"
        verbose_name_plural = "時間割"

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "department",
                    "course",
                    "target_grade",
                    "target_class_number",
                    "weekday",
                    "start_period",
                ],
                name="unique_lecture_slot_for_target",
            )
        ]

    def __str__(self):
        return (
            f"{self.subject}（"
            f"{self.get_weekday_display()} "
            f"{self.start_period.period}〜{self.end_period.period}限 "
            f"{self.get_status_display()}）"
        )

    def clean(self):
        errors = {}

        # 入力途中（admin対策）
        if not all([
            self.start_period_id,
            self.end_period_id,
            self.department_id,
        ]):
            return

        # ① 開始 <= 終了
        if self.start_period.period > self.end_period.period:
            errors["end_period"] = "終了時限は開始時限以降でなければなりません。"

        # ② 時限の重なりチェック（休講は枠を占有しない）
        overlapping_qs = LectureSchedule.objects.filter(
            department=self.department,
            target_grade=self.target_grade,
            target_class_number=self.target_class_number,
            weekday=self.weekday,
            start_period__period__lte=self.end_period.period,
            end_period__period__gte=self.start_period.period,
        ).exclude(status=LectureSchedule.Status.CANCELED)

        # course の NULL 比較
        if self.course_id:
            overlapping_qs = overlapping_qs.filter(course=self.course)
        else:
            overlapping_qs = overlapping_qs.filter(course__isnull=True)

        # 更新時は自分自身を除外
        if self.pk:
            overlapping_qs = overlapping_qs.exclude(pk=self.pk)

        if overlapping_qs.exists():
            errors["start_period"] = "この時限帯には既に別の授業が登録されています。"

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# ==========================================================
# お知らせモデル
# ==========================================================

# 受信メール


class ReceivedEmail(models.Model):
    subject = models.CharField(max_length=255)      # 件名
    sender = models.EmailField()                    # 送信元メールアドレス
    body = models.TextField()                       # 本文
    message_uid = models.CharField(                 # IMAP UID
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    received_at = models.DateTimeField(              # 受信日時
        null=True,
        blank=True
    )
    target_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,  # 学科が削除されても、お知らせ自体は消さない設定
        related_name='announcements',
        null=True,
        blank=True,
        verbose_name="対象学科"
    )
    target_grade = models.PositiveIntegerField(
        choices=Profile.GRADE_CHOICES,
        null=True,
        blank=True,
        verbose_name="対象学年"
    )

    def __str__(self):
        return self.subject

# ==========================================================
# イベントモデル
# ==========================================================


class Event(models.Model):

    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    target_department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None
    )

    target_grade = models.PositiveIntegerField(
        choices=Profile.GRADE_CHOICES,
        null=True,
        blank=True,
        default=None
    )

    is_external = models.BooleanField(
        default=False,
        db_index=True,
        help_text="学外向けイベントかどうか（False=学内向け）",
    )

    class Meta:
        ordering = ["is_external", "start_date", "end_date"]

    def __str__(self):
        scope = "学外" if self.is_external else "学内"

        dept = (
            self.target_department.name
            if self.target_department
            else "全学科"
        )

        grade = (
            self.get_target_grade_display()
            if self.target_grade is not None
            else "全学年"
        )

        if self.start_date == self.end_date:
            date_str = self.start_date
        else:
            date_str = f"{self.start_date}〜{self.end_date}"

        return f"[{scope}｜{dept} {grade}] {self.title}（{date_str}）"
