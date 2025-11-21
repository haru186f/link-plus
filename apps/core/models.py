from django.db import models


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
    campus_departure = models.TimeField(blank=True, null=True)                 # キャンパス発の時刻（登校）
    campus_arrival = models.TimeField(blank=True, null=True)                   # キャンパス着の時刻
    station_departure = models.TimeField(blank=True, null=True)                # 駅発の時刻（下校）
    note = models.CharField(max_length=100, blank=True, null=True)             # 備考
    is_saturday = models.BooleanField(default=False)                           # 平日か土曜日

    # 外部キー
    bus_stop = models.ForeignKey(       # バス停（八王子か八王子みなみ野）
        BusStop,
        on_delete=models.CASCADE,
        related_name="bus_schedules"
        )

    def __str__(self):
        if self.station_departure:
            direction = "登校"
            time = self.station_departure
        elif self.campus_departure:
            direction = "下校"
            time = self.campus_departure

        time_str = time.strftime("%H:%M")

        return f"{self.bus_stop}（{'土曜' if self.is_saturday else '平日'}・{direction}）: {time_str}"


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
    name = models.CharField(max_length=100)     # 学科名
    max_grade = models.IntegerField(default=4)  # 最大学年（デフォルトは４年）

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
    received_at = models.DateTimeField(auto_now_add=True)   # 受信日時

    def __str__(self):
        return self.subject
