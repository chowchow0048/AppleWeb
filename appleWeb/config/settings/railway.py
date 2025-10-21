from .base import *
import os

# Railway DATABASE_URL 파싱용 (설치된 경우에만 import)
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# DEBUG 설정 - Railway 환경변수에서 가져오기
DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "yes", "on"]

# Railway 환경에서 제공되는 도메인 자동 추가
railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
railway_static_url = os.environ.get("RAILWAY_STATIC_URL")

# ALLOWED_HOSTS 초기화 (base.py에서 빈 리스트로 설정됨)
ALLOWED_HOSTS = []

if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)
if railway_static_url:
    ALLOWED_HOSTS.append(railway_static_url)


# 데이터베이스 설정 - .env 파일 수동 로딩
env_file = BASE_DIR / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                # 따옴표 제거
                value = value.strip("\"'")
                os.environ.setdefault(key, value)

# ALLOWED_HOSTS: 환경변수에서 추가 도메인 가져오기
allowed_hosts_str = os.environ.get("ALLOWED_HOSTS")
if allowed_hosts_str:
    additional_hosts = [
        host.strip() for host in allowed_hosts_str.split(",") if host.strip()
    ]
    ALLOWED_HOSTS.extend(additional_hosts)

# Railway 기본 도메인들 추가 (안전장치)
if not ALLOWED_HOSTS:
    # Railway 기본 패턴 허용 (프로덕션에서는 실제 도메인 설정 필요)
    ALLOWED_HOSTS = [
        "*.up.railway.app",  # Railway 기본 도메인
        "127.0.0.1",
        "localhost",
    ]
    print(
        "WARNING: Using default ALLOWED_HOSTS. Set ALLOWED_HOSTS environment variable for production."
    )

# 세션 설정
SESSION_COOKIE_AGE = 7200
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# 기본 데이터베이스 설정은 아래 PostgreSQL 설정 섹션에서 처리

# 미디어 파일 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"

# CKEditor 업로드 경로
CKEDITOR_UPLOAD_PATH = "uploads/"

# SECRET_KEY: 환경변수 필수 (보안 강화)
secret_key = os.environ.get("DJANGO_SECRET_KEY")
if not secret_key:
    raise ValueError(
        "DJANGO_SECRET_KEY environment variable is required for security. "
        "Generate a new secret key and set it in your .env file."
    )
DJANGO_SECRET_KEY = secret_key

# ===========================
# 정적 파일 설정 (Railway 최적화)
# ===========================

# 정적 파일 URL (슬래시로 시작해야 함)
STATIC_URL = "/static/"

# 정적 파일 경로 설정
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic이 파일을 수집할 경로
STATICFILES_DIRS = [BASE_DIR / "static"]  # 개발 시 정적 파일 경로

# WhiteNoise 미들웨어 추가 (정적 파일 서빙)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# 정적 파일 압축 및 캐싱 (성능 최적화)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# WhiteNoise 설정
WHITENOISE_USE_FINDERS = False  # 프로덕션에서는 False
WHITENOISE_AUTOREFRESH = False  # 프로덕션에서는 False
WHITENOISE_MAX_AGE = 31536000  # 1년 캐싱

# ===========================
# 데이터베이스 설정 (PostgreSQL)
# ===========================

# Railway PostgreSQL 연결 설정
database_url = os.environ.get("DATABASE_URL")
if database_url and dj_database_url:
    # dj_database_url로 DATABASE_URL 파싱 (Railway 표준 방식)
    DATABASES = {
        "default": dj_database_url.parse(
            database_url,
            conn_max_age=600,  # 연결 풀링 최적화
            conn_health_checks=True,  # 연결 상태 확인
        )
    }
else:
    # PostgreSQL 환경 변수가 있는지 확인
    pg_host = os.environ.get("PGHOST")
    if pg_host:
        # 환경 변수 개별 설정 (백업용)
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("PGDATABASE", "railway"),
                "USER": os.environ.get("PGUSER", "postgres"),
                "PASSWORD": os.environ.get("PGPASSWORD", ""),
                "HOST": pg_host,
                "PORT": os.environ.get("PGPORT", "5432"),
                "OPTIONS": {
                    "connect_timeout": 10,  # 연결 타임아웃
                    "options": "-c default_transaction_isolation=read_committed",
                },
            }
        }
    else:
        # PostgreSQL이 설정되지 않은 경우 SQLite 사용 (빌드 단계용)
        print("INFO: Using SQLite fallback (build phase or development)")
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
                "OPTIONS": {
                    "timeout": 20,
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
    TEMPLATES[0]["APP_DIRS"] = False  # loaders 사용시 APP_DIRS는 False여야 함
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
