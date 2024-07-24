from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("signup/", views.signup_view, name="user_signup"),
    path("get-coordinates/", views.get_coordinates, name="get_coordinates"),
    path("", views.user_list_view, name="user_list"),  # 사용자 목록 페이지(for testing)
]
