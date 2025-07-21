# Railway 배포용 설정 파일
import os
import dj_database_url
from .base import *

# 환경 변수를 통한 설정 관리
# Railway에서 제공하는 환경 변수들을 사용

# SECRET_KEY를 환경 변수로 관리 (보안 강화)
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-ebved*q!zji3wjbw8@!--f&wxra#oyn(9nqko1)@khxwm0vh$2"
)

# 프로덕션 모드
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Railway에서 자동으로 RAILWAY_PUBLIC_DOMAIN 환경 변수를 제공
# 추가로 커스텀 도메인도 설정 가능
ALLOWED_HOSTS = [
    ".up.railway.app",  # Railway 기본 도메인
    "banpo-apple.com",  # 커스텀 도메인
    "www.banpo-apple.com",  # 커스텀 도메인
    "127.0.0.1",  # 로컬 테스트용
    "localhost",  # 로컬 테스트용
]

# Railway 환경에서 RAILWAY_PUBLIC_DOMAIN이 제공되면 추가
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)

# 정적 파일 설정 (Railway에서는 WhiteNoise 미들웨어 사용)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise 미들웨어 추가 (정적 파일 서빙용)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# 정적 파일 압축 및 캐싱
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 데이터베이스 설정 - Railway PostgreSQL
# Railway는 DATABASE_URL 환경 변수를 자동으로 제공
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # dj_database_url을 사용하여 DATABASE_URL 파싱
    DATABASES = {"default": dj_database_url.parse(database_url, conn_max_age=600)}
else:
    # 환경 변수가 없을 경우 개별 DB 설정 사용
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_NAME", "railway"),
            "USER": os.environ.get("DB_USER", "postgres"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

# 보안 설정 (HTTPS 환경)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# 세션 설정
SESSION_COOKIE_AGE = 7200  # 2시간
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

# 미디어 파일 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CKEditor 업로드 경로
CKEDITOR_UPLOAD_PATH = "uploads/"

# 로깅 설정 (Railway 환경에 맞게 조정)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "appleWeb": {
            "handlers": ["console"],
            "level": os.environ.get("APP_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

# APScheduler 설정 - Railway 환경에서는 Redis 사용 권장
SCHEDULER_DEFAULT = True

# Railway에서는 Redis URL이 제공될 수 있음
redis_url = os.environ.get("REDIS_URL")
if redis_url:
    # Redis를 캐시 백엔드로 사용
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
