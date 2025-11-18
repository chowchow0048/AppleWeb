from .base import *
import os

STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = []

DEBUG = False

env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                # 따옴표 제거
                value = value.strip("\"'")
                os.environ.setdefault(key, value)

allowed_hosts_str = os.environ.get("ALLOWED_HOSTS")
if not allowed_hosts_str:
    raise ValueError(
        "ALLOWED_HOSTS environment variable is required for security. "
        "Set it to your domain names (e.g., 'example.com,www.example.com')"
    )
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(",") if host.strip()]

# SESSION_COOKIE_AGE = 24000000000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}

# 미디어 파일 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# CKEditor 업로드 경로
CKEDITOR_UPLOAD_PATH = "uploads/"

# SECRET_KEY: 환경변수 필수 (보안 강화)
secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise ValueError(
        "SECRET_KEY environment variable is required for security. "
        "Generate a new secret key and set it in your .env file."
    )
SECRET_KEY = secret_key
