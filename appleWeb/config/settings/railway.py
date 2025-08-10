# Railway 배포용 설정 파일
import os
import dj_database_url
from .base import *

# ===========================
# 기본 Django 설정 오버라이드
# ===========================

# SECRET_KEY를 환경 변수로 관리 (보안 강화)
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-railway-fallback-key-change-in-production"
)

# 프로덕션 모드 설정
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Railway 도메인 및 커스텀 도메인 허용
ALLOWED_HOSTS = [
    "*",  # Railway는 동적 도메인을 사용하므로 모든 호스트 허용
    ".up.railway.app",  # Railway 기본 도메인
    "banpo-apple.com",  # 커스텀 도메인
    "www.banpo-apple.com",  # 커스텀 도메인 www
    "127.0.0.1",  # 로컬 테스트
    "localhost",  # 로컬 테스트
]

# Railway 환경에서 제공되는 도메인 자동 추가
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)

# ===========================
# 정적 파일 설정 (WhiteNoise)
# ===========================

# 정적 파일 경로 설정
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# WhiteNoise 미들웨어 추가 (정적 파일 서빙)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# 정적 파일 압축 및 캐싱 (성능 최적화)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ===========================
# 데이터베이스 설정 (PostgreSQL)
# ===========================

# Railway PostgreSQL 연결 설정
database_url = os.environ.get("DATABASE_URL")
if database_url:
    # dj_database_url로 DATABASE_URL 파싱 (Railway 표준 방식)
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,  # 연결 풀링 최적화
            conn_health_checks=True,  # 연결 상태 확인
        )
    }
else:
    # 환경 변수 개별 설정 (백업용)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("PGDATABASE", "railway"),
            "USER": os.environ.get("PGUSER", "postgres"),
            "PASSWORD": os.environ.get("PGPASSWORD", ""),
            "HOST": os.environ.get("PGHOST", "localhost"),
            "PORT": os.environ.get("PGPORT", "5432"),
            "OPTIONS": {
                "connect_timeout": 10,  # 연결 타임아웃
                "options": "-c default_transaction_isolation=read_committed",
            },
        }
    }

# ===========================
# 보안 설정 (HTTPS 환경)
# ===========================

# 프로덕션 환경에서만 보안 설정 활성화
if not DEBUG:
    # HTTPS 관련 보안 설정
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # 추가 보안 헤더
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1년
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ===========================
# 세션 설정
# ===========================

SESSION_COOKIE_AGE = 7200  # 2시간 (기존 설정 유지)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 브라우저 닫아도 세션 유지
SESSION_SAVE_EVERY_REQUEST = True  # 활동 시 세션 연장
SESSION_COOKIE_HTTPONLY = True  # XSS 공격 방지
SESSION_COOKIE_SAMESITE = "Lax"  # CSRF 공격 방지

# ===========================
# 미디어 파일 설정
# ===========================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CKEditor 업로드 경로
CKEDITOR_UPLOAD_PATH = "uploads/"

# ===========================
# 로깅 설정 (Railway 최적화)
# ===========================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {module} {message}",
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
            "level": "INFO",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.environ.get("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_console"],
            "level": "ERROR",
            "propagate": False,
        },
        "appleWeb": {
            "handlers": ["console"],
            "level": os.environ.get("APP_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        # 스케줄러 로깅 (APScheduler)
        "apscheduler": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# ===========================
# 캐시 설정 (Redis 사용 가능시)
# ===========================

redis_url = os.environ.get("REDIS_URL")
if redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {
                    "max_connections": 20,
                    "retry_on_timeout": True,
                },
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            },
            "KEY_PREFIX": "appleWeb",
            "TIMEOUT": 300,  # 5분 기본 캐시 타임아웃
        }
    }

    # 세션을 Redis에 저장 (성능 향상)
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    # Redis가 없으면 데이터베이스 캐시 사용
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "django_cache_table",
        }
    }

# ===========================
# APScheduler 설정
# ===========================

# 스케줄러 기본 설정 유지
SCHEDULER_DEFAULT = True
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# Railway 환경에서는 단일 인스턴스 실행 권장
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # 타임아웃 설정

# ===========================
# 이메일 설정 (필요시 활성화)
# ===========================

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# ===========================
# 성능 최적화 설정
# ===========================

# 데이터베이스 연결 최적화
CONN_MAX_AGE = 600  # 10분 연결 유지

# 템플릿 캐싱 (프로덕션에서만)
if not DEBUG:
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        (
            "django.template.loaders.cached.Loader",
            [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        ),
    ]

# ===========================
# Railway 특화 설정
# ===========================

# Railway의 빌드 및 배포 최적화
USE_TZ = True
TIME_ZONE = "Asia/Seoul"
LANGUAGE_CODE = "ko-kr"

# Railway 환경 변수 디버깅 (개발시에만 사용)
if DEBUG:
    print("=== Railway Environment Variables ===")
    for key, value in os.environ.items():
        if key.startswith(("RAILWAY_", "DATABASE_", "REDIS_")):
            print(f"{key}: {value}")
    print("=====================================")
