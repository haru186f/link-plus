"""
開発用設定 (Development Settings)
"""

from config.settings.base import * # base.py の共通設定を読み込む
from dotenv import load_dotenv
import os

# ==========================================================
# 環境変数の読み込み(.env.development)
# ==========================================================

load_dotenv(BASE_DIR / ".env.development", override=True)  # 開発環境用の.envファイルを読み込む
SECRET_KEY = os.getenv('SECRET_KEY')        # 環境変数からSECRET_KEYを取得

# ==========================================================
# デバッグ設定
# ==========================================================

DEBUG = True    # 開発中は詳細なエラーメッセージを表示

# ==========================================================
# 許可するホスト
# ==========================================================

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']   # ローカル環境でのアクセスを許可

# ==========================================================
# データベース設定（PostgreSQL 共通）
# ==========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',                  # PostgreSQLを使用
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),               # データベース名
        'USER': os.getenv('POSTGRES_USER', 'postgres'),             # DBユーザー名
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),     # パスワード
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),            # ホスト名
        'PORT': os.getenv('POSTGRES_PORT', '5432'),                 # ポート番号
    }
}

# ==========================================================
# Django Debug Toolbar 設定
# ==========================================================

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

    # SecurityMiddleware の直後に追加
    index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware') + 1
    MIDDLEWARE.insert(index, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    INTERNAL_IPS = ['127.0.0.1', 'localhost']

# ==========================================================
# メールサーバー接続設定 (IMAP) 
# ==========================================================

# IMAP接続情報 (環境変数から読み込む)
# 実際のメールアドレスとパスワードは .env.development に設定してください
EMAIL_IMAP_HOST = os.getenv('EMAIL_IMAP_HOST', 'imap.example.com')  # ホスト名
EMAIL_IMAP_PORT = int(os.getenv('EMAIL_IMAP_PORT', 993))            # ポート番号 (int型に変換)
EMAIL_IMAP_USER = os.getenv('EMAIL_IMAP_USER', None)                      # ユーザー名/メールアドレス
EMAIL_IMAP_PASS = os.getenv('EMAIL_IMAP_PASS', None)                      # パスワード
