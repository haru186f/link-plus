"""
本番用設定 (Production Settings)
"""

from config.settings.base import * # base.py（共通設定）を読み込む
from dotenv import load_dotenv
import os

# ==========================================================
# 環境変数の読み込み（.env.production）
# ==========================================================

load_dotenv(BASE_DIR / ".env.production")
SECRET_KEY = os.getenv("SECRET_KEY")

# ==========================================================
# デバッグ設定
# ==========================================================

DEBUG = False   # 本番環境ではエラーページなどに内部情報を表示しない

# ==========================================================
# 許可するホスト
# ==========================================================

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# ==========================================================
# 静的ファイル設定
# ==========================================================

STATIC_ROOT = BASE_DIR / "staticfiles"
# collectstatic コマンドで全ての静的ファイルをこのフォルダに集約
# 本番デプロイ前に必ず「python manage.py collectstatic」を実行

# ==========================================================
# セキュリティ設定
# ==========================================================

CSRF_COOKIE_SECURE = True               # HTTPS通信でのみCSRFクッキーを送信
SESSION_COOKIE_SECURE = True            # HTTPS通信でのみセッションクッキーを送信
SECURE_HSTS_SECONDS = 31536000          # HSTSを1年間適用（HTTPS通信を強制）
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # サブドメインにもHSTSを適用
SECURE_HSTS_PRELOAD = True              # HSTSプリロード対応
SECURE_SSL_REDIRECT = True              # HTTPアクセスをHTTPSに自動リダイレクト

# ==========================================================
# メール設定（必要なら追加）
# ==========================================================

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
# EMAIL_USE_TLS = True
