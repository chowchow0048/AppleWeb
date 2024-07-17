from django.urls import path
from . import views

urlpatterns = [
    path("", views.community_home, name="community_home"),
    path("notice/", views.community_notice, name="community_notice"),
    path(  # 데일리 페이지 수업 불러오기 api
        "api/courses/", views.api_courses, name="api_courses"
    ),
]
