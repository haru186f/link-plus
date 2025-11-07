from django.db import models
from apps.accounts.models import Bus

class BusSchedule(models.Model):
    campus_departure = models.TimeField(blank=True, null=True)                 # キャンパス発
    station_departure = models.TimeField(blank=True, null=True)                # 駅発
    campus_arrival = models.TimeField(blank=True, null=True)                   # キャンパス着
    note = models.CharField(max_length=100, blank=True, null=True)             # 備考

    is_saturday = models.BooleanField(default=False)                           # 平日 or 土曜日

    bus = models.ForeignKey('accounts.Bus', on_delete=models.CASCADE)                     # 八王子 or 八王子みなみ野

    def __str__(self):
        # 方向を自動判定
        if self.station_departure:
            direction = "登校"
            time = self.station_departure
        elif self.campus_departure:
            direction = "下校"
            time = self.campus_departure
        else:
            direction = "-"
            time = self.campus_arrival

        time_str = time.strftime("%H:%M") if time else "-"

        return f"{self.bus.name}（{'土曜' if self.is_saturday else '平日'}・{direction}）: {time_str}"
