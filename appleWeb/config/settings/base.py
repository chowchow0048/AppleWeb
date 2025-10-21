from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECRET_KEY = "django-insecure-development-key-change-in-production-12345"
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "yes", "on"]

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "common.User"
SESSION_COOKIE_AGE = 7200
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True

LOGIN_URL = "/user/login/"

# Application definition
INSTALLED_APPS = [
    "common",
    "main",
    "community",
    "management",
    "django_apscheduler",
    "widget_tweaks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ckeditor_5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 20,
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

NAVER_CLIENT_ID = "v2uy1n9cc7"
NAVER_CLIENT_SECRET = "SgFqv8FBOrYyCjmym4InxD6Daig1yHvhDr68F2vz"

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d: %(message)s"
        },
    },
    "handlers": {
        "console_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "console.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "django_server_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "django_server.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "app_file": {
            "level": "DEBUG",
            "filters": ["require_debug_false"],
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "appleWeb.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "standard",
        },
        "payment_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "payment.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "detailed",
        },
        "scheduler_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "scheduler.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "detailed",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console_file", "mail_admins", "app_file"],
            "level": "DEBUG",
        },
        "django.server": {
            "handlers": ["django_server_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "appleWeb": {
            "handlers": ["app_file"],
            "level": "DEBUG",
        },
        "appleWeb.payment": {
            "handlers": ["payment_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "appleWeb.scheduler": {
            "handlers": ["scheduler_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
        ],
        "height": 400,
        "width": "auto",
        "image": {
            "toolbar": ["imageTextAlternative", "imageStyle:full", "imageStyle:side"],
        },
        "link": {
            "addTargetToExternalLinks": True,
        },
    },
    "extends": {
        "toolbar": "full",
        "width": "100%",
    },
}

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
SCHEDULER_DEFAULT = True
