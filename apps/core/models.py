from django.db import models

from apps.accounts.models import Profile

# ==========================================================
# バスモデル
# ==========================================================

# バス停
class BusStop(models.Model):
    BUS_CHOICES = [('hachiouji', '八王子'), ('minamino', '八王子みなみ野')]

    name = models.CharField(max_length=20, choices=BUS_CHOICES, default='hachiouji')    # バス停の名前

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


# 教室
class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 時間割
class SchoolPeriod(models.Model):
    period = models.PositiveIntegerField()      # 時限
    start_time = models.TimeField()     # 開始時刻
    end_time = models.TimeField()       # 終了時刻

    class Meta:
        ordering = ['period']

    def __str__(self):
        return f"{self.period}限（{self.start_time}-{self.end_time}）"


# 講義スケジュール
class LectureSchedule(models.Model):

    DAY_OF_WEEK_CHOICES = [
        ("mon", "月"),
        ("tue", "火"),
        ("wed", "水"),
        ("thu", "木"),
        ("fri", "金"),
    ]

    name = models.CharField(max_length=100)             # 講義名
    start_period = models.PositiveIntegerField()        # 開始時限
    end_period = models.PositiveIntegerField()          # 終了時限
    day_of_week = models.CharField(                     # 曜日
        max_length=10,
        choices=DAY_OF_WEEK_CHOICES
    )
    is_canceled = models.BooleanField(default=False)

    # 外部キー
    department = models.ForeignKey(    # 学科 (必須)
        Department,
        on_delete=models.CASCADE,
        related_name='lecture_schedules',
        # コースがない場合の時間割はdepartmentで絞り込む
    )
    course = models.ForeignKey(         # コース (オプション)
        Course,
        on_delete=models.CASCADE,
        related_name='lecture_schedules',
        null=True,                      # コースがない学科に対応
        blank=True
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='lecture_schedules'
    )
    # 学年 (必須)
    target_grade = models.PositiveIntegerField(
        choices=Profile.GRADE_CHOICES,
    )

    # クラス (必須)
    target_class_number = models.PositiveIntegerField(
        choices=Profile.CLASS_CHOICES,
    )


    @property
    def day_label(self):
        """choices の label(日本語) を返す"""
        return dict(self.DAY_OF_WEEK_CHOICES).get(self.day_of_week, "")

    def __str__(self):
        return f"{self.name}（{self.day_label}曜日・{self.start_period}〜{self.end_period}限）"

    @property
    def start_time(self):
        return SchoolPeriod.objects.get(period=self.start_period).start_time

    @property
    def end_time(self):
        return SchoolPeriod.objects.get(period=self.end_period).end_time



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

    def __str__(self):
        return self.subject
