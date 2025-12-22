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
        "grade": 2,
        "class": 1,
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

DAY_MAPPING = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
}

class Command(BaseCommand):
    help = "講義スケジュールをデータベースへ登録します"

    @transaction.atomic
    def handle(self, *args, **options):

        # ==============================
        # カレッジと学科を作成/取得
        # ==============================
        college, _ = College.objects.get_or_create(name="ITカレッジ")

        # Departmentオブジェクトを取得/作成
        department, _ = Department.objects.get_or_create(
            name="情報処理科",
            defaults={"college": college, "max_grade": 2}
        )
        self.stdout.write(self.style.SUCCESS(f"学科: {department.name} を確認/作成しました。"))

        # ==============================
        # 教室を作成/取得
        # ==============================
        room_obj, created_room = Room.objects.get_or_create(name="B-601")

        if created_room:
            self.stdout.write(self.style.SUCCESS("Room B-601 を新規作成しました"))
        else:
            self.stdout.write(self.style.WARNING("Room B-601 はすでに存在します"))

        created = 0

        for lec in LECTURE_DATA:

            # 講義データが特定の教室に依存している場合 (ここではB-601に限定)
            if lec["room"] != room_obj.name:
                continue

            # 必須項目がデータに存在するかチェック
            required_keys = ["grade", "class", "day"]
            if not all(key in lec for key in required_keys):
                self.stdout.write(self.style.ERROR(f"データセットに必須キーがありません: {lec['name']}"))
                continue

            # 曜日文字列を整数値に変換
            weekday_int = DAY_MAPPING.get(lec["day"])
            if weekday_int is None:
                self.stdout.write(self.style.ERROR(f"無効な曜日指定 '{lec['day']}' があります: {lec['name']}"))
                continue


            # ==============================
            # コースが存在すれば作成/取得（department を必ず紐付け）
            # ==============================
            course_name = lec.get("course")
            course = None

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
            # LectureSchedule 登録/更新
            # ==============================

            # 登録前に、ユニーク制約で使われるキーをすべて抽出して存在チェックを行う
            # (LectureScheduleにget_or_createがないため、存在チェックのみ行う)
            try:
                # ユニーク制約 (department, course, target_grade, target_class_number, weekday, start_period)
                existing_lecture = LectureSchedule.objects.get(
                    department=department,
                    course=course,
                    target_grade=lec["grade"],
                    target_class_number=lec["class"],
                    weekday=weekday_int,
                    start_period=lec["start"],
                )
                self.stdout.write(self.style.WARNING(f"講義 '{lec['name']}' ({lec['day']}{lec['start']}限) は既に存在します。スキップします。"))
                continue

            except LectureSchedule.DoesNotExist:
                # 存在しない場合、新規作成
                LectureSchedule.objects.create(
                    subject=lec["name"], # <== フィールド名を subject に修正
                    weekday=weekday_int, # <== フィールド名を weekday に修正し、整数値を使用
                    start_period=lec["start"],
                    end_period=lec["end"],
                    room=room_obj,

                    # 絞り込みキー
                    department=department,
                    course=course,
                    target_grade=lec["grade"],
                    target_class_number=lec["class"],

                    # teacherフィールドが必須ではないため、ここではNone（未設定）のまま
                )

                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"{created} 件の B-601 講義スケジュールを新規登録しました！"
        ))
