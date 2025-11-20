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

# 정적 파일 설정
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Django 5.0+ STORAGES 설정 (ManifestStaticFilesStorage)
# 파일명에 해시값 추가로 캐시 무효화 자동 처리
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static/images"

CKEDITOR_UPLOAD_PATH = "uploads/"  # 이미지 업로드 시 사용할 경로
