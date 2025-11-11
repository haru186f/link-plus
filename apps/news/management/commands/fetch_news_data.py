import imaplib
import email
from email.header import decode_header
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.news.models import ReceivedEmail
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'IMAPサーバーからメールを取得してデータベースに保存します。'

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=10, help='取得する最新メール件数（デフォルト10件）')
        parser.add_argument('--folder', type=str, default='INBOX', help='取得対象フォルダ（デフォルトINBOX）')

    def handle(self, *args, **options):
        # 🚨 IMAP接続に必要な設定を settings.py から取得
        host = getattr(settings, 'EMAIL_IMAP_HOST', None)
        port = getattr(settings, 'EMAIL_IMAP_PORT', 993)
        user = getattr(settings, 'EMAIL_IMAP_USER', None)
        password = getattr(settings, 'EMAIL_IMAP_PASS', None)
        limit = options['limit']
        folder = options['folder']

        # 設定確認
        if not all([host, user, password]):
            self.stderr.write(self.style.ERROR("❌ IMAP設定が不完全です。settings.py の EMAIL_IMAP_* を確認してください。"))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(f"📬 {user} ({host}) から最新 {limit} 件のメールを取得します..."))

        mail = None
        saved_count = 0
        
        try:
            # --- IMAP接続とログイン ---
            self.stdout.write("接続中...")
            mail = imaplib.IMAP4_SSL(host, port)
            mail.login(user, password)
            self.stdout.write(self.style.SUCCESS("✅ ログイン成功"))
            mail.select(folder)

            # --- メール検索 ---
            status, data = mail.search(None, 'ALL') 
            if status != 'OK':
                raise Exception(f"メール検索に失敗しました。ステータス: {status}")

            mail_ids = data[0].split()
            if not mail_ids:
                self.stdout.write(self.style.WARNING("⚠️ メールがありません。"))
                return

            # 最新N件に絞り込み
            mail_ids = mail_ids[-limit:]
            
            # --- メール解析と保存 ---
            for mail_id in mail_ids:
                # 既存のメールIDチェックを省略しているため、重複保存される可能性がありますが、
                # まずは表示確認を優先し、このまま進めます。
                
                status, msg_data = mail.fetch(mail_id, '(RFC822)')
                if status != 'OK':
                    logger.warning(f"メール {mail_id} の取得に失敗しました。")
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # 件名、送信者、本文の抽出ロジック（前回の成功コードと同じ）
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                sender = msg.get("From", "Unknown Sender")
                
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get("Content-Disposition", ""))
                        if ctype == "text/plain" and "attachment" not in cdispo:
                            charset = part.get_content_charset() or "utf-8"
                            body = part.get_payload(decode=True).decode(charset, errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                # DBに保存
                ReceivedEmail.objects.create(
                    subject=subject or "(No Subject)",
                    sender=sender,
                    body=body or "(Empty Body)",
                    # received_at はモデルで auto_now_add=True のため省略
                )
                saved_count += 1

            self.stdout.write(self.style.SUCCESS(f"✅ {saved_count} 件のメールを保存しました。"))

        except imaplib.IMAP4.error as e:
            self.stderr.write(self.style.ERROR(f"IMAP認証エラー: {e}。ユーザー名/パスワード/ホストを確認してください。"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ 処理中に予期せぬエラーが発生しました: {e}"))
        finally:
            if mail:
                try:
                    mail.logout()
                except:
                    pass