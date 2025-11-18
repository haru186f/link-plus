from django.core.management.base import BaseCommand
from apps.core.models import College, Department, Course


class Command(BaseCommand):
    help = "カレッジ・学科・コースの初期データを追加します"

    def handle(self, *args, **options):
        # 既存データ削除
        self.stdout.write(self.style.WARNING("⚠ 既存のカレッジ・学科・コースを削除中..."))
        Course.objects.all().delete()
        Department.objects.all().delete()
        College.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("データをすべて削除しました。新しいデータを登録します。"))

        # ------------------------------
        # クリエイターズカレッジ
        # ------------------------------
        creators_college = College.objects.create(name="クリエイターズカレッジ")

        # 放送芸術科
        dept_broadcast = Department.objects.create(name="放送芸術科", college=creators_college)
        Course.objects.bulk_create([
            Course(name="カメラマンコース", department=dept_broadcast),
            Course(name="制作コース", department=dept_broadcast),
            Course(name="映像編集コース", department=dept_broadcast),
            Course(name="音声コース", department=dept_broadcast),
            Course(name="照明コース", department=dept_broadcast),
            Course(name="美術コース", department=dept_broadcast),
        ])

        # 声優・演劇科
        dept_voice = Department.objects.create(name="声優・演劇科", college=creators_college)
        Course.objects.bulk_create([
            Course(name="声優コース", department=dept_voice),
            Course(name="俳優・タレントコース", department=dept_voice),
        ])

        # 演劇スタッフ科
        dept_acting = Department.objects.create(name="演劇スタッフ科", college=creators_college)
        Course.objects.bulk_create([
            Course(name="舞台監督専攻", department=dept_acting),
            Course(name="舞台美術専攻", department=dept_acting),
            Course(name="舞台照明専攻", department=dept_acting),
            Course(name="舞台音響専攻", department=dept_acting),
            Course(name="2.5次元舞台専攻", department=dept_acting),
        ])

        # マンガ・アニメーション科（4年制）
        dept_manga4 = Department.objects.create(name="マンガ・アニメーション科（4年制）", college=creators_college)
        Course.objects.bulk_create([
            Course(name="キャラクターデザインコース", department=dept_manga4),
            Course(name="マンガコース", department=dept_manga4),
            Course(name="アニメーションコース", department=dept_manga4),
            Course(name="マンガ・アニメビジネスコース", department=dept_manga4),
        ])

        # マンガ・アニメーション科
        dept_manga2 = Department.objects.create(name="マンガ・アニメーション科", college=creators_college)
        Course.objects.bulk_create([
            Course(name="キャラクターデザインコース", department=dept_manga2),
            Course(name="マンガコース", department=dept_manga2),
            Course(name="アニメーションコース", department=dept_manga2),
        ])

        # ------------------------------
        # デザインカレッジ
        # ------------------------------
        design_college = College.objects.create(name="デザインカレッジ")

        # ゲームクリエイター科（4年制）
        dept_game4 = Department.objects.create(name="ゲームクリエイター科（4年制）", college=design_college)
        Course.objects.bulk_create([
            Course(name="ゲームプログラマーコース", department=dept_game4),
            Course(name="ゲームプランナーコース", department=dept_game4),
        ])

        # ゲームクリエイター科（3年制）
        dept_game3 = Department.objects.create(name="ゲームクリエイター科（3年制）", college=design_college)

        # ゲームプログラミング科
        dept_prog = Department.objects.create(name="ゲームプログラミング科", college=design_college)

        # CG映像科（3年制）
        dept_cg = Department.objects.create(name="CG映像科（3年制）", college=design_college)
        Course.objects.bulk_create([
            Course(name="ゲームCG専攻", department=dept_cg),
            Course(name="アニメCG専攻", department=dept_cg),
            Course(name="映像・VFX専攻", department=dept_cg),
        ])

        # デザイン科（3年制）
        dept_design = Department.objects.create(name="デザイン科（3年制）", college=design_college)
        Course.objects.bulk_create([
            Course(name="グラフィックデザイン専攻", department=dept_design),
            Course(name="イラストレーション専攻", department=dept_design),
            Course(name="インテリアデザイン専攻", department=dept_design),
            Course(name="プロダクトデザイン専攻", department=dept_design),
        ])

        # ------------------------------
        # ミュージックカレッジ
        # ------------------------------
        music_college = College.objects.create(name="ミュージックカレッジ")

        # ミュージックアーティスト科
        dept_artist = Department.objects.create(name="ミュージックアーティスト科", college=music_college)
        Course.objects.bulk_create([
            Course(name="プレイヤーコース", department=dept_artist),
            Course(name="ヴォーカリストコース", department=dept_artist),
            Course(name="サウンドクリエイターコース", department=dept_artist),
        ])

        # コンサート・イベント科
        dept_concert = Department.objects.create(name="コンサート・イベント科", college=music_college)
        Course.objects.bulk_create([
            Course(name="コンサート制作コース", department=dept_concert),
            Course(name="コンサートPAコース", department=dept_concert),
            Course(name="コンサート照明コース", department=dept_concert),
            Course(name="コンサート舞台コース", department=dept_concert),
            Course(name="イベント企画コース", department=dept_concert),
        ])

        # 音響芸術科
        dept_music_art = Department.objects.create(name="音響芸術科", college=music_college)
        Course.objects.bulk_create([
            Course(name="レコーディングエンジニア専攻", department=dept_music_art),
            Course(name="MAエンジニア専攻", department=dept_music_art),
            Course(name="ラジオスタッフ専攻", department=dept_music_art),
        ])

        # ダンスパフォーマンス科
        dept_dance = Department.objects.create(name="ダンスパフォーマンス科", college=music_college)
        Course.objects.bulk_create([
            Course(name="プロダンサー専攻", department=dept_dance),
            Course(name="バックダンサー専攻", department=dept_dance),
            Course(name="ダンス＆ヴォーカル専攻", department=dept_dance),
            Course(name="コレオグラファー(振付)専攻", department=dept_dance),
            Course(name="ダンスインストラクター専攻", department=dept_dance),
            Course(name="テーマパークダンサー専攻", department=dept_dance),
        ])

        # ------------------------------
        # ITカレッジ
        # ------------------------------
        it_college = College.objects.create(name="ITカレッジ")

        # ITスペシャリスト科（4年制）
        dept_it_specialist = Department.objects.create(name="ITスペシャリスト科（4年制）", college=it_college)
        Course.objects.bulk_create([
            Course(name="AI・システム専攻", department=dept_it_specialist),
            Course(name="ネットワーク・クラウド専攻", department=dept_it_specialist),
            Course(name="セキュリティ専攻", department=dept_it_specialist),
        ])

        # AIシステム科
        dept_ai = Department.objects.create(name="AIシステム科", college=it_college)
        dept_info_proc = Department.objects.create(name="情報処理科", college=it_college)
        Course.objects.bulk_create([
            Course(name="システム開発コース", department=dept_info_proc),
            Course(name="モバイルアプリ開発コース", department=dept_info_proc),
            Course(name="システム運用コース", department=dept_info_proc),
        ])

        # ネットワークセキュリティ科
        dept_network = Department.objects.create(name="ネットワークセキュリティ科", college=it_college)
        Course.objects.bulk_create([
            Course(name="ネットワーク専攻", department=dept_network),
            Course(name="セキュリティ専攻", department=dept_network),
        ])

        # 情報ビジネス科
        dept_biz = Department.objects.create(name="情報ビジネス科", college=it_college)
        Course.objects.bulk_create([
            Course(name="秘書・事務コース", department=dept_biz),
            Course(name="eビジネスコース", department=dept_biz),
        ])

        # ホテル・観光科
        dept_hotel = Department.objects.create(name="ホテル・観光科", college=it_college)
        Course.objects.bulk_create([
            Course(name="観光マーケティングコース", department=dept_hotel),
            Course(name="ホテルスタッフコース", department=dept_hotel),
        ])

        # ------------------------------
        # テクノロジーカレッジ
        # ------------------------------
        college_tech = College.objects.create(name="テクノロジーカレッジ")

        # 電子・電気科
        dept_elec = Department.objects.create(name="電子・電気科", college=college_tech)
        Course.objects.bulk_create([
            Course(name="電子工学コース／電子工学専攻", department=dept_elec),
            Course(name="電子工学コース／オーディオ・家電専攻", department=dept_elec),
            Course(name="電子工学コース／スマート技術専攻", department=dept_elec),
            Course(name="電気工学コース／電気工学専攻", department=dept_elec),
            Course(name="電気工学コース／エネルギー管理士専攻", department=dept_elec),
            Course(name="電気工事コース／電気工事士専攻", department=dept_elec),
            Course(name="電気工事コース／電気工事施工管理専攻", department=dept_elec),
        ])

        # ロボット科
        dept_robot = Department.objects.create(name="ロボット科", college=college_tech)
        Course.objects.bulk_create([
            Course(name="ロボット制御プログラム専攻", department=dept_robot),
            Course(name="ロボット制作専攻", department=dept_robot),
            Course(name="二足歩行ロボット専攻", department=dept_robot),
            Course(name="パーツメンテナンス専攻", department=dept_robot),
        ])

        # 機械設計科
        dept_machine = Department.objects.create(name="機械設計科", college=college_tech)

        # 一級自動車整備科（4年制）
        dept_auto_4 = Department.objects.create(name="一級自動車整備科（4年制）", college=college_tech)

        # 自動車整備科
        dept_auto_2 = Department.objects.create(name="自動車整備科", college=college_tech)

        # 建築学科（4年制）
        dept_arch_4 = Department.objects.create(name="建築学科（4年制）", college=college_tech)
        Course.objects.bulk_create([
            Course(name="BIM・デジタルデザイン専攻", department=dept_arch_4),
            Course(name="建築・インテリア設計専攻", department=dept_arch_4),
            Course(name="建築構造・設備専攻", department=dept_arch_4),
            Course(name="建築施工専攻", department=dept_arch_4),
        ])

        # 建築設計科
        dept_arch = Department.objects.create(name="建築設計科", college=college_tech)
        Course.objects.bulk_create([
            Course(name="BIM・デジタルデザイン専攻", department=dept_arch),
            Course(name="建築・インテリア設計専攻", department=dept_arch),
            Course(name="建築構造・設備専攻", department=dept_arch),
            Course(name="建築施工専攻", department=dept_arch),
        ])

        # 土木・造園科
        dept_civil = Department.objects.create(name="土木・造園科", college=college_tech)

        # 応用生物学科
        dept_bio = Department.objects.create(name="応用生物学科", college=college_tech)
        Course.objects.bulk_create([
            Course(name="医薬品専攻", department=dept_bio),
            Course(name="食品専攻", department=dept_bio),
            Course(name="化粧品専攻", department=dept_bio),
        ])

        # ------------------------------
        # スポーツ・医療カレッジ
        # ------------------------------
        sports_college = College.objects.create(name="スポーツ・医療カレッジ")

        # スポーツトレーナー科（3年制）
        dept_train3 = Department.objects.create(name="スポーツトレーナー科（3年制）", college=sports_college)
        Course.objects.bulk_create([
            Course(name="アスレティックトレーナーコース", department=dept_train3),
            Course(name="パーソナルトレーナーコース", department=dept_train3),
            Course(name="メディカルトレーナーコース", department=dept_train3),
        ])

        # スポーツ健康学科（3年制）
        dept_medi_train3 = Department.objects.create(name="スポーツ健康学科（3年制）", college=sports_college)
        Course.objects.bulk_create([
            Course(name="スポーツインストラクターコース／スタジオフィットネス専攻", department=dept_medi_train3),
            Course(name="スポーツインストラクターコース／レジャースポーツ専攻", department=dept_medi_train3),
            Course(name="スポーツインストラクターコース／チャイルドスポーツ専攻", department=dept_medi_train3),
            Course(name="スポーツビジネスコース／イベント専攻", department=dept_medi_train3),
            Course(name="スポーツビジネスコース／販売専攻", department=dept_medi_train3),
            Course(name="サッカーコース／マリノス強化専攻", department=dept_medi_train3),
            Course(name="サッカーコース／コーチ・指導者・審判専攻", department=dept_medi_train3),
            Course(name="テニスコース／テニス専攻", department=dept_medi_train3),
            Course(name="テニスコース／ソフトテニス専攻", department=dept_medi_train3),
            Course(name="バスケットボールコース／プレイヤー専攻", department=dept_medi_train3),
            Course(name="スケットボールコース／コーチ・指導者・審判専攻", department=dept_medi_train3),
        ])

        # スポーツ健康学科
        dept_medi_train = Department.objects.create(name="スポーツ健康学科", college=sports_college)
        Course.objects.bulk_create([
            Course(name="スポーツインストラクターコース／スタジオフィットネス専攻", department=dept_medi_train),
            Course(name="スポーツインストラクターコース／レジャースポーツ専攻", department=dept_medi_train),
            Course(name="スポーツインストラクターコース／チャイルドスポーツ専攻", department=dept_medi_train),
            Course(name="スポーツビジネスコース／イベント専攻", department=dept_medi_train),
            Course(name="スポーツビジネスコース／販売専攻", department=dept_medi_train),
            Course(name="サッカーコース／マリノス強化専攻", department=dept_medi_train),
            Course(name="サッカーコース／コーチ・指導者・審判専攻", department=dept_medi_train),
            Course(name="テニスコース／テニス専攻", department=dept_medi_train),
            Course(name="テニスコース／ソフトテニス専攻", department=dept_medi_train),
            Course(name="バスケットボールコース／プレイヤー専攻", department=dept_medi_train),
            Course(name="スケットボールコース／コーチ・指導者・審判専攻", department=dept_medi_train),
        ])

        # 鍼灸整（3年制）
        dept_acu = Department.objects.create(name="鍼灸科（3年制）", college=sports_college)
        Course.objects.bulk_create([
            Course(name="スポーツ鍼灸コース", department=dept_acu),
            Course(name="美容鍼灸コース", department=dept_acu),
            Course(name="整体コース", department=dept_acu),
        ])

        # 柔道整復科（3年制）
        dept_therapy = Department.objects.create(name="柔道整復科（3年制）", college=sports_college)

        self.stdout.write(self.style.SUCCESS("✅ カレッジ・学科・コースの初期データを追加しました！"))
