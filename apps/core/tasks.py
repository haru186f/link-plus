import imaplib
import email
from email.header import decode_header
from datetime import datetime
import pytz # タイムゾーン処理のため
from django.conf import settings
from .models import ReceivedEmail

def fetch_and_save_emails():
    # 接続情報 (settings.pyから取得)
    IMAP_HOST = settings.EMAIL_IMAP_HOST
    IMAP_USER = settings.EMAIL_IMAP_USER
    IMAP_PASS = settings.EMAIL_IMAP_PASS

    # 既に保存されているUIDのリストを取得
    existing_uids = ReceivedEmail.objects.values_list('message_uid', flat=True)

    try:
        # **🔥 デバッグポイント 1: 接続開始 🔥**
        print("--- デバッグ: IMAP接続を開始します ---")
        # 1. IMAPサーバーへ接続
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(IMAP_USER, IMAP_PASS)
        # **🔥 デバッグポイント 2: ログイン成功 🔥**
        print("--- デバッグ: IMAPログインに成功しました ---")
        mail.select('inbox') # 取得するフォルダを選択

        # 2. すべてのメールのUIDを取得
        # 'ALL'の代わりに 'UNSEEN' などを使用すれば未読のみ対象にできます
        status, messages = mail.uid('search', None, 'FROM', 'link-hac@g.neec.ac.jp') #特定のメールアドレス
        if status != 'OK':
            print(f"メール検索に失敗しました: {status}")
            return

        uids = messages[0].split()

        # 3. 未保存のメールをループして処理
        for uid_byte in uids:
            uid = uid_byte.decode()

            # **重複チェックのロジック (ポイント)**
            if uid in existing_uids:
                continue # 既にDBにあるためスキップ

            # UIDでメールデータをFETCH (RFC822: メール全体)
            status, msg_data = mail.uid('fetch', uid_byte, '(RFC822)')
            if status != 'OK':
                print(f"UID {uid} のFETCHに失敗しました: {status}")
                continue

            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # 4. メールデータの解析
            subject, encoding = decode_header(msg['Subject'])[0]
            if encoding:
                subject = subject.decode(encoding)

            sender_info = email.utils.parseaddr(msg['From'])
            sender_address = sender_info[1] # 送信元のメールアドレス

            # 受信日時の解析
            date_tuple = email.utils.parsedate_tz(msg['date'])
            if date_tuple:
                local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                # タイムゾーン情報を付加
                received_at = pytz.utc.localize(local_date) if local_date.tzinfo is None else local_date
            else:
                received_at = datetime.now(pytz.timezone(settings.TIME_ZONE)) # 解析失敗時は現在時刻

            # 本文の抽出 (マルチパート対応)
            body_text = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    cdisp = str(part.get("Content-Disposition"))

                    # テキストパート（インライン添付ファイルでないもの）を抽出
                    if ctype == 'text/plain' and 'attachment' not in cdisp:
                        try:
                            charset = part.get_content_charset() or 'utf-8'
                            body_text = part.get_payload(decode=True).decode(charset, errors='ignore')
                            break # 最初のプレーンテキストを本文として採用
                        except:
                            continue
            else:
                # シングルパートの場合
                charset = msg.get_content_charset() or 'utf-8'
                body_text = msg.get_payload(decode=True).decode(charset, errors='ignore')


            # 5. DBに保存
            ReceivedEmail.objects.create(
                message_uid=uid,
                subject=subject,
                sender=sender_address,
                body=body_text,
                received_at=received_at
            )
            print(f"メールUID {uid} をDBに保存しました。")

    except Exception as e:
        print(f"メール処理中にエラーが発生しました: {e}")
    finally:
        if 'mail' in locals() and mail:
            mail.logout()
