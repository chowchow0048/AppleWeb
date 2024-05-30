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


# 로그인 처리 뷰
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
            # 로그인
            login(request, user)
            # 지정한 페이지로 redirect
            return redirect("community_home")
        # 유효하지 않다면
        else:
            # 아이디 틀렸을 때, 비밀번호 틀렸을 때 추가?
            # 로그인 페이지로 redirect
            return render(
                request,
                "user/user_login.html",
                {"error": "아이디 혹은 비밀번호가 올바르지 않습니다"},
            )
    # GET 요청이 들어왔을 때
    else:
        # 로그인 페이지 render
        return render(request, "user/user_login.html")


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


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.integrated_science = request.POST.get("integrated_science") == "on"
            user.physics = request.POST.get("physics") == "on"
            user.chemistry = request.POST.get("chemistry") == "on"
            user.biology = request.POST.get("biology") == "on"
            user.earth_science = request.POST.get("earth_science") == "on"

            user.save()

            messages.success(request, "관리자의 승인 후 계정이 활성화됩니다.")
            return redirect("user_login")
        else:
            # 폼 전체 에러 메시지 추가
            for error in form.non_field_errors():
                messages.error(request, error)
                # messages.error(
                #     request,
                #     f'integrated: {request.POST.get("integrated_science")}, physics: {request.POST.get("physics")}, chemistry: {request.POST.get("chemistry")}, biology: {request.POST.get("biology")}, earth_science: {request.POST.get("earth_science")}',
                # )

            # 폼 필드별 에러 메시지 추가
            for field, errors in form.errors.items():
                if field != "__all__":
                    for error in errors:
                        field_label = (
                            form.fields[field].label
                            if field in form.fields
                            else "Error"
                        )
                        messages.error(request, f"{field_label}: {error}")

            return render(request, "user/user_signup.html", {"form": form})
    else:
        form = SignUpForm()
        return render(request, "user/user_signup.html", {"form": form})


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
