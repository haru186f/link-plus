from django.core.management.base import BaseCommand
from django.db import transaction
from apps.core.models import LectureSchedule, Course, Room, College, Department


# ============================================
# 登録する講義データ（ハードコード）
# ============================================
# LECTURE_DATAはそのまま使用
LECTURE_DATA = [
    {
        "name": "キャリアデザイン4",
        "day": "mon",
        "start": 1,
        "end": 2,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2, # 新しいフィールド
        "class": 1, # 新しいフィールド
    },
    {
        "name": "Webセキュリティ実習",
        "day": "mon",
        "start": 3,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "卒業制作２",
        "day": "mon",
        "start": 5,
        "end": 8,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "ITプロモーション",
        "day": "tue",
        "start": 2,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "卒業制作２",
        "day": "tue",
        "start": 5,
        "end": 8,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "プログラミング実習３",
        "day": "thu",
        "start": 1,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "卒業制作２",
        "day": "wed",
        "start": 1,
        "end": 4,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
    },
    {
        "name": "情報資格対策講座４",
        "day": "fri",
        "start": 5,
        "end": 6,
        "room": "B-601",
        "course": "システム開発コース",
        "grade": 2,
        "class": 1,
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

        # Departmentオブジェクトを取得/作成 (LectureScheduleへの紐づけに必要)
        department, _ = Department.objects.get_or_create(
            name="情報処理科",
            defaults={"college": college, "max_grade": 2}
        )
        self.stdout.write(self.style.SUCCESS(f"学科: {department.name} を確認/作成しました。"))

        # ==============================
        # B-601 を作成
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

            # 必須項目がデータに存在するかチェック
            if not all(key in lec for key in ["grade", "class"]):
                 self.stdout.write(self.style.ERROR(f"データセットに 'grade' または 'class' がありません: {lec['name']}"))
                 continue


            # ==============================
            # コースが存在すれば作成（department を必ず紐付け）
            # ==============================
            course_name = lec.get("course") # courseがない場合も考慮して.get()を使用
            course = None # courseがNoneの場合も許容

            if course_name:
                course, course_created = Course.objects.get_or_create(
                    name=course_name,
                    defaults={"department": department}
                )

                if course_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Course '{course_name}' を新規作成しました")
                    )

            # ==============================
            # LectureSchedule 追加 (修正箇所)
            # ==============================
            LectureSchedule.objects.create(
                name=lec["name"],
                day_of_week=lec["day"],
                start_period=lec["start"],
                end_period=lec["end"],
                room=room_obj,

                # 新しい絞り込みキー
                department=department,                  # <== 学科オブジェクト
                course=course,                          # <== コースオブジェクト (Noneの場合もある)
                target_grade=lec["grade"],              # <== 学年 (int)
                target_class_number=lec["class"],       # <== クラス (int)
            )

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created} 件の B-601 講義スケジュールを登録しました！"
        ))
