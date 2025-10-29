"""
共通設定 (Base Settings)
開発・本番の両方で共通して使う基本設定をまとめています。
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================================
# 基本パス設定
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==========================================================
# アプリケーション設定
# ==========================================================

INSTALLED_APPS = [
    # アプリケーション
    'apps.accounts',

    # デフォルト
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==========================================================
# テンプレート設定
# ==========================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==========================================================
# URL / WSGI 設定
# ==========================================================

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

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
# 認証
# ==========================================================

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.UsernameOrEmailBackend',  # ユーザー名 or メールでログイン
    'django.contrib.auth.backends.ModelBackend',      # Django標準（管理画面など）
]

# ==========================================================
# パスワードバリデーション
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================================================
# 国際化設定
# ==========================================================

LANGUAGE_CODE = 'ja'        # 日本語
TIME_ZONE = 'Asia/Tokyo'    # 日本時間
USE_I18N = True             # 国際化対応を有効化
USE_TZ = True               # タイムゾーンを有効化

# ==========================================================
# 静的ファイル設定
# ==========================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ==========================================================
# デフォルト設定
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
