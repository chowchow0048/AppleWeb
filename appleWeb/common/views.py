from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import User
from .forms import SignUpForm
import requests


@never_cache
def user_logout(request):
    logout(request)
    return redirect("main_home")


def ajax_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": "Authentication failed"})


# 로그인 뷰
def login_view(request):
    # POST 요청일 때만 로그인 시도
    if request.method == "POST":
        # 폼으로부터 사용자 이름과 비밀번호 가져오기
        username = request.POST["username"]
        password = request.POST["password"]
        # authenticate 함수: req, username, password를 유효한지 확인
        user = authenticate(request, username=username, password=password)
        # 유효하다면
        if user is not None:
            # 계정이 활성화된 경우
            if user.is_active:
                # 로그인
                login(request, user)
                # 지정한 페이지로 redirect
                # return redirect("community_home")
                return redirect("management_home")
            # 계정이 활성화되지 않은 경우
            else:
                print("비활성화게정")
                return render(
                    request,
                    "user/user_login.html",
                    {"error": "활성화되지 않은 계정입니다."},
                )
        # 사용자가 유효하지 않다면
        else:
            # 아이디와 비밀번호가 맞지 않음
            try:
                # 사용자 객체를 가져와서 비활성화 여부 확인
                user = User.objects.get(username=username)
                if not user.is_active:
                    print("비활성화계정")
                    return render(
                        request,
                        "user/user_login.html",
                        {"error": "활성화되지 않은 계정입니다."},
                    )
            except User.DoesNotExist:
                pass

            print("아이디비번틀림")
            return render(
                request,
                "user/user_login.html",
                {"error": "아이디 혹은 비밀번호가 올바르지 않습니다"},
            )
    # GET 요청이 들어왔을 때
    else:
        # 로그인 페이지 render
        return render(request, "user/user_login.html", {})


# 사용자 목록 뷰
@login_required
def user_list_view(request):
    # 로그인한 유저가 staff라면
    if request.user.is_staff:
        # 모든 사용자의 목록을 가져온다
        users = User.objects.all()
        # 가져온 사용자 목록 render
        return render(request, "user/user_list.html", {"users": users})
    # 로그인한 유저가 staff가 아니라면
    else:
        # 로그인 페이지로 redirect
        return redirect("user_login")


# 주소 변환
def get_coordinates(request):
    query = "서울특별시 서초구 신반포로 189 반포쇼핑타운 4동 402호"
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": settings.NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        location_data = response.json()
        print(location_data)
        return render(
            request, "main/get-coordinates.html", {"location_data": location_data}
        )
    except requests.exceptions.HTTPError as e:
        # 에러 로그 출력, HTTP 에러에 대응
        print(f"HTTP Error: {e}")
        return render(
            request,
            "main.html",
            {"error": "Location data could not be retrieved due to an HTTP Error."},
        )
    except requests.exceptions.ConnectionError as e:
        # 네트워크 문제 관련 에러 처리
        print(f"Connection Error: {e}")
        return render(
            request,
            "main/get-coordinates.html",
            {
                "error": "Location data could not be retrieved due to a Connection Error."
            },
        )
    except requests.exceptions.Timeout as e:
        # 요청 시간 초과 에러 처리
        print(f"Timeout Error: {e}")
        return render(
            request,
            "main/get-coordinates.html",
            {"error": "Location data could not be retrieved due to a Timeout."},
        )
    except requests.exceptions.RequestException as e:
        # 그 외 요청 예외 처리
        print(f"Request Exception: {e}")
        return render(
            request,
            "main/get-coordinates.html",
            {
                "error": "Location data could not be retrieved due to an unspecified Error."
            },
        )


def page_not_found(request, exception):
    return render(request, "main/404.html", {})


def server_error(request):
    # 임시: 500 에러 디버깅을 위해 간단한 응답
    from django.http import HttpResponse
    import traceback
    import sys

    # 실제 에러 정보 가져오기
    exc_info = sys.exc_info()
    error_message = "".join(traceback.format_exception(*exc_info)) if exc_info[0] else "No exception info"

    return HttpResponse(
        f"<h1>500 Server Error (Debug)</h1><pre>{error_message}</pre>",
        status=500
    )


def forbidden_error(request, exception):
    return render(request, "main/403.html", {})


def bad_request(request, exception):
    return render(request, "main/400.html", {})


import logging

logger = logging.getLogger("appleWeb")


def log_view(request):
    logger.info("INFO 레벨로 출력")
