from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),  # 로그인 페이지
    path(
        "users/", views.user_list_view, name="user_list"
    ),  # 사용자 목록 페이지(testing)
]
