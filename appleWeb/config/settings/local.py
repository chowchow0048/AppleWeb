from .base import *

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "appleWeb"),
        "USER": os.environ.get("DB_USER", "chow"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

SESSION_COOKIE_AGE = 72000

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static/images"

CKEDITOR_UPLOAD_PATH = "uploads/"  # 이미지 업로드 시 사용할 경로
