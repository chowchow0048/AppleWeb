import os
from .base import *

# 로컬 환경에서는 DEBUG를 True로 강제 설정합니다.
# base.py에서 이미 DEBUG가 설정되어 있으므로 여기서 다시 설정해야 합니다.
DEBUG = os.environ.get("DEBUG", "True").lower() in ["true", "1", "yes", "on"]

# 환경 변수에서 ALLOWED_HOSTS_LOCAL 값을 읽어옵니다.
# 로컬 환경에서는 기본값으로 localhost와 127.0.0.1을 허용합니다.
ALLOWED_HOSTS_LOCAL = os.environ.get("ALLOWED_HOSTS_LOCAL", "127.0.0.1,localhost")

# 쉼표로 구분된 호스트 목록을 파싱하여 리스트로 변환합니다.
if ALLOWED_HOSTS_LOCAL:
    ALLOWED_HOSTS = [
        host.strip() for host in ALLOWED_HOSTS_LOCAL.split(",") if host.strip()
    ]
else:
    # DEBUG가 False이고 ALLOWED_HOSTS_LOCAL이 설정되지 않은 경우 빈 리스트로 설정
    # Django가 에러를 발생시켜 사용자에게 설정을 요구하도록 합니다.
    ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SESSION_COOKIE_AGE = 72000

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "static/images"

CKEDITOR_UPLOAD_PATH = "uploads/"  # 이미지 업로드 시 사용할 경로
