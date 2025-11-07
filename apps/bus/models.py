from django.db import models
from apps.accounts.models import Bus

class BusSchedule(models.Model):
    DIRECTION_CHOICES = [
        ('to_school', '登校'),
        ('from_school', '下校'),
    ]

    campus_departure = models.TimeField(blank=True, null=True)                 # キャンパス発
    station_departure = models.TimeField(blank=True, null=True)                # 駅発
    campus_arrival = models.TimeField(blank=True, null=True)                   # キャンパス着
    note = models.CharField(max_length=100, blank=True, null=True)             # 備考

    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)     # 登校 or 下校
    is_saturday = models.BooleanField(default=False)                           # 平日 or 土曜日

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)                     # 八王子 or 八王子みなみ野
