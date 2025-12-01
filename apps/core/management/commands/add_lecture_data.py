from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import LectureSchedule, Course, Room, College, Department


# ============================================
# 登録する講義データ（ハードコード）
# ============================================
LECTURE_DATA = [
    {
        "name": "キャリアデザイン4",
        "day": "mon",
        "start": 1,
        "end": 2,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "Webセキュリティ実習",
        "day": "mon",
        "start": 3,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "卒業制作２",
        "day": "mon",
        "start": 5,
        "end": 8,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "ITプロモーション",
        "day": "tue",
        "start": 2,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "卒業制作２",
        "day": "tue",
        "start": 5,
        "end": 8,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "プログラミング実習３",
        "day": "thu",
        "start": 1,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "卒業制作２",
        "day": "wed",
        "start": 1,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
    },
    {
        "name": "情報資格対策講座４",
        "day": "fri",
        "start": 5,
        "end": 6,
        "room": "B-601",
        "course": "システム開発コース",
    },
]


class Command(BaseCommand):
    help = "講義スケジュールをデータベースへ登録します"

    @transaction.atomic
    def handle(self, *args, **options):

        # ==============================
        # カレッジと学科を作成
        # ==============================
        college, _ = College.objects.get_or_create(name="ITカレッジ")
        department, _ = Department.objects.get_or_create(
            name="情報処理科",
            defaults={"college": college, "max_grade": 2}
        )

        # ==============================
        # B-601 を最初に作成
        # ==============================
        room_obj, created_room = Room.objects.get_or_create(name="B-601")

        if created_room:
            self.stdout.write(self.style.SUCCESS("Room B-601 を新規作成しました"))
        else:
            self.stdout.write(self.style.WARNING("Room B-601 はすでに存在します"))

        created = 0

        for lec in LECTURE_DATA:

            if lec["room"] != "B-601":
                continue

            # ==============================
            # コースが存在しなければ作成（department を必ず紐付け）
            # ==============================
            course_name = lec["course"]
            course, course_created = Course.objects.get_or_create(
                name=course_name,
                defaults={"department": department}
            )

            if course_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Course '{course_name}' を新規作成しました")
                )

            # ==============================
            # LectureSchedule 追加
            # ==============================
            LectureSchedule.objects.create(
                name=lec["name"],
                day_of_week=lec["day"],
                start_period=lec["start"],
                end_period=lec["end"],
                course=course,
                room=room_obj,
            )

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created} 件の B-601 講義スケジュールを登録しました！"
        ))
