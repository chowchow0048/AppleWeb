import environ
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

ALLOWED_HOSTS = [
    "3.37.147.68",
    "banpo-apple.com",
    "www.banpo-apple.com",
    "ec2-3-37-147-68.ap-northeast-2.compute.amazonaws.com",
]
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = []

DEBUG = False

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
