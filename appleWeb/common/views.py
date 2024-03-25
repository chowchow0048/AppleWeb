from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User


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
            return redirect("user_list")
        # 유효하지 않다면
        else:
            # 아이디 틀렸을 때, 비밀번호 틀렸을 때 추가?
            # 로그인 페이지로 redirect
            return render(
                request,
                "users/login.html",
                {"error": "아이디 혹은 비밀번호가 올바르지 않습니다"},
            )
    # GET 요청이 들어왔을 때
    else:
        # 로그인 페이지 render
        return render(request, "accounts/login.html")


# 사용자 목록 뷰
@login_required
def user_list_view(request):
    # 로그인한 유저가 staff라면
    if request.user.is_staff:
        # 모든 사용자의 목록을 가져온다
        users = User.objects.all()
        # 가져온 사용자 목록 render
        return render(request, "users/user_list.html", {"users": users})
    # 로그인한 유저가 staff가 아니라면
    else:
        # 로그인 페이지로 redirect
        return redirect("login")
