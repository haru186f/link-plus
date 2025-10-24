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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 開発アプリはここに追加
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
# データベース（個別環境で上書きするため、ここでは空）
# ==========================================================

DATABASES = {
    'default': {}
}

# ==========================================================
# 認証・パスワードバリデーション
# ==========================================================

LOGIN_REDIRECT_URL = '/'

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
# 静的ファイル設定（開発環境で使用）
# ==========================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # 開発用

# ==========================================================
# デフォルト設定
# ==========================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
