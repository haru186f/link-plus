import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = "すべてのカスタムコマンドを自動的に実行します。"

    def handle(self, *args, **options):
        apps_dir = os.path.join(settings.BASE_DIR, "apps")

        all_commands = []

        # apps 以下の全アプリを探索
        for app_name in os.listdir(apps_dir):
            app_path = os.path.join(apps_dir, app_name)

            if not os.path.isdir(app_path):
                continue

            commands_dir = os.path.join(app_path, "management", "commands")

            # commands ディレクトリが存在するアプリのみ対象
            if not os.path.isdir(commands_dir):
                continue

            # コマンドファイル名の抽出（_始まりと自身を除外）
            command_files = [
                f[:-3]
                for f in os.listdir(commands_dir)
                if f.endswith(".py")
                and not f.startswith("_")
                and f[:-3] != "run_all_custom_commands"
            ]

            all_commands.extend(command_files)

        # コマンド一覧表示
        self.stdout.write(self.style.NOTICE("=== 検出されたカスタムコマンド一覧 ==="))
        for cmd in all_commands:
            self.stdout.write(f" - {cmd}")
        self.stdout.write("")

        # 各コマンドを順番に実行
        for cmd in all_commands:
            self.stdout.write(self.style.NOTICE(f"▶ 実行中: {cmd}"))
            call_command(cmd)
            self.stdout.write(self.style.SUCCESS(f"✔ 完了: {cmd}"))
            self.stdout.write("")  # 見やすさのため空行

        self.stdout.write(self.style.SUCCESS("🎉 すべてのカスタムコマンドが正常に完了しました"))
