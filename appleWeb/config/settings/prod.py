import environ
from .base import *

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

ALLOWED_HOSTS = ["3.37.147.68", "banpo-apple.com", "www.banpo-apple.com"]
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

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static/images/review"
