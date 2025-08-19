import environ
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = []

SESSION_COOKIE_AGE = 7200
# 추가된 부분
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": "5432",
    }
}

# CKEditor에서 파일을 업로드하는 경로 (미디어 파일)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# CKEditor 업로드 경로
CKEDITOR_UPLOAD_PATH = "uploads/"
