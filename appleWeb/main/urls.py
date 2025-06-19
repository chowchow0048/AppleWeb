from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main_home"),
    path("notice/<int:id>", views.notice_detail, name="notice_detail"),
    path("review/<int:id>", views.review_detail, name="review_detail"),
    path("notice_data/", views.notice_data, name="notice_data"),
]
