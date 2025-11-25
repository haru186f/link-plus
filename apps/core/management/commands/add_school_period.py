from django.core.management.base import BaseCommand
from apps.core.models import SchoolPeriod
import datetime


PERIOD_DATA = [
    (1, "09:30", "10:15"),
    (2, "10:15", "11:00"),
    (3, "11:10", "11:55"),
    (4, "11:55", "12:40"),
    (5, "13:30", "14:15"),
    (6, "14:15", "15:00"),
    (7, "15:10", "15:55"),
    (8, "15:55", "16:40"),
]


class Command(BaseCommand):
    help = "SchoolPeriod（時間割）データを登録します。"

    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING("時間割データを登録します…"))

        for period, start, end in PERIOD_DATA:
            start_time = datetime.time.fromisoformat(start)
            end_time = datetime.time.fromisoformat(end)

            obj, created = SchoolPeriod.objects.update_or_create(
                period=period,
                defaults={
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"  追加: {period}限 {start}〜{end}"))
            else:
                self.stdout.write(self.style.NOTICE(f"  更新: {period}限 {start}〜{end}"))

        self.stdout.write(self.style.SUCCESS("完了しました！"))
