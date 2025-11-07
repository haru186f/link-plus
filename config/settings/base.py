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
    'apps.home.apps.HomeConfig',            # その他のアプリ（設定、天気、マップ等）
    'apps.lecture.apps.LectureConfig',      # 講義
    'apps.news.apps.NewsConfig',            # お知らせ
    'apps.bus.apps.BusConfig',              # バス時刻
    'apps.accounts.apps.AccountsConfig',    # 認証関係

    # デフォルト
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ライブラリ
    'django_extensions',
    'django_crontab',
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
# データベース設定（PostgreSQL 共通、ここで上書き）
# ==========================================================

DATABASES = {}

# ==========================================================
# 認証
# ==========================================================

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_REDIRECT_URL = '/home/'
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

# ==========================================================
# django-crontab 設定
# ==========================================================

CRONJOBS = [

]

# 例：
# 毎朝6時に天気APIを更新
# ('0 6 * * *', 'apps.core.cron.fetch_weather'),

# 10分ごとにバス時刻表を更新
# ('*/10 * * * *', 'apps.bus.cron.fetch_bus_timetable'),

# 毎朝8時に定期メールを送信
# ('0 8 * * *', 'apps.core.cron.send_daily_mail'),
