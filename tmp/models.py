from django.db import models
from apps.accounts.models import Bus

class BusSchedule(models.Model):
    DIRECTION_CHOICES = [
        ('to_school', '登校'),
        ('from_school', '下校'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    departure_time = models.TimeField()
    is_weekend = models.BooleanField(default=False)

    class Meta:
        ordering = ["bus", "direction", "departure_time"]
