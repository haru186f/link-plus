"""
本番用設定 (Production Settings)
"""

from config.settings.base import * # base.py（共通設定）を読み込む
from dotenv import load_dotenv
import os

# ==========================================================
# デバッグ設定
# ==========================================================

DEBUG = False   # 本番環境ではエラーページなどに内部情報を表示しない

# ==========================================================
# 環境変数 (.env.production) の読み込み
# ==========================================================

load_dotenv(BASE_DIR / ".env.production")  # 本番環境用の環境変数を読み込む
SECRET_KEY = os.getenv("SECRET_KEY")    # 環境変数からSECRET_KEYを取得

# ==========================================================
# 許可するホスト
# ==========================================================

ALLOWED_HOSTS = []  # 本番環境のドメインを許可

# ==========================================================
# データベース設定
# ==========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',          # PostgreSQLを使用
        'NAME': os.getenv('POSTGRES_DB'),                   # データベース名
        'USER': os.getenv('POSTGRES_USER'),                 # DBユーザー名
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),         # パスワード
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),    # ホスト名
        'PORT': os.getenv('POSTGRES_PORT', '5432'),         # ポート番号
    }
}

# ==========================================================
# 静的ファイル（CSS, JS, 画像など）の設定
# ==========================================================

STATIC_ROOT = BASE_DIR / "staticfiles"
# collectstaticコマンドで全ての静的ファイルをこのフォルダに集約
# RenderやPythonAnywhereの「静的ファイル配信設定」でこのパスを指定する
# 本番デプロイ前に必ず「python manage.py collectstatic」を実行する

# ==========================================================
# セキュリティ設定
# ==========================================================

CSRF_COOKIE_SECURE = True        # HTTPSでのみCSRFクッキーを送信
SESSION_COOKIE_SECURE = True     # HTTPSでのみセッションクッキーを送信
SECURE_HSTS_SECONDS = 31536000   # HTTPSを強制（1年間）
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True       # HTTPアクセスをHTTPSにリダイレクト

# ==========================================================
# メール設定（必要なら追加）
# ==========================================================

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = os.getenv('EMAIL_PORT')
# EMAIL_HOST_USER = os.getenv('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
# EMAIL_USE_TLS = True
