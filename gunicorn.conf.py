#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Gunicorn 설정 파일 - Railway 배포용

import multiprocessing
import os

# 서버 설정
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"  # Railway에서 PORT 환경 변수 사용
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # 최대 4개 워커
worker_class = "sync"  # 동기 워커 사용
worker_connections = 1000
max_requests = 1000  # 메모리 누수 방지를 위해 요청 수 제한
max_requests_jitter = 100  # 무작위 지터 추가
preload_app = True  # 앱 미리 로드로 메모리 절약

# 타임아웃 설정
timeout = 120  # 요청 타임아웃 (초)
keepalive = 2  # Keep-alive 연결 시간 (초)
graceful_timeout = 30  # Graceful 종료 대기 시간 (초)

# 로깅 설정
loglevel = "info"
accesslog = "-"  # stdout으로 로그 출력
errorlog = "-"  # stderr로 오류 로그 출력
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 프로세스 이름
proc_name = "appleWeb"

# 보안 설정
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 성능 최적화
forwarded_allow_ips = "*"  # Railway 로드 밸런서 허용
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}

# Railway 환경에서 디버그 정보
if os.environ.get("RAILWAY_ENVIRONMENT") == "production":
    print(f"🚀 Running on Railway with {workers} workers")
    print(f"📊 Binding to {bind}")
    print(f"🔒 HTTPS headers configured")
else:
    print(f"🔧 Development mode with {workers} workers")
    print(f"📊 Binding to {bind}")
