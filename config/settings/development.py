"""
開発用設定 (Development Settings)
"""

from config.settings.base import * # base.py の共通設定を読み込む
from dotenv import load_dotenv
import os

# ==========================================================
# 環境変数 (.envdevelopment) の読み込み
# ==========================================================

load_dotenv(BASE_DIR / ".env.development")  # 開発環境用の.envファイルを読み込む
SECRET_KEY = os.getenv('SECRET_KEY')    # 環境変数からSECRET_KEYを取得

# ==========================================================
# デバッグ設定
# ==========================================================

DEBUG = True    # 開発中は詳細なエラーメッセージを表示

# ==========================================================
# 許可するホスト
# ==========================================================

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']   # ローカル環境でのアクセスを許可

# ==========================================================
# データベース設定
# ==========================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# メールやキャッシュなどの開発用設定
# ==========================================================

# 開発時にメール送信を確認したい場合は次のように設定可能
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# → メール内容がコンソールに出力される
