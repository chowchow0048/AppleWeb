# appleWeb/management/urls.py 파일에 추가
from django.urls import path
from . import views

urlpatterns = [
    path("", views.management_home, name="management_home"),
    path("student-list/", views.management_studentlist, name="management_studentlist"),
    path(
        "student-list/<int:course_id>/",
        views.management_studentlist_detail,
        name="management_studentlist_detail",
    ),  # 출석부 상세 페이지 URL
    # path(
    #     "student-list2/<int:course_id>/",
    #     views.management_studentlist_detail2,
    #     name="management_studentlist_detail2",
    # ),  # 출석부 상세 페이지 URL 수정중
    path("bulk_attendance/", views.bulk_attendance, name="bulk_attendance"),
    path(
        "student_detail/<int:student_id>/",
        views.management_student_detail,
        name="management_student_detail",
    ),
    path("pay-list/", views.management_paylist, name="management_paylist"),
    path("wait-list/", views.management_waitList, name="management_waitlist"),
    path("black-list/", views.management_blacklist, name="management_blacklist"),
    # path("notice", views.management_notice, name="management_notice"),
    path("api/courses/", views.api_courses, name="api_courses"),
    path("api/students/", views.api_students, name="api_students"),
    path("api/record_attendance/", views.record_attendance, name="record_attendance"),
    path("api/record_absence/", views.record_absence, name="record_absence"),
    path(
        "confirm-payment/<int:user_id>/", views.confirm_payment, name="confirm_payment"
    ),
    path(
        "export_attendance/<int:course_id>/",
        views.export_attendance_to_excel,
        name="export_attendance",
    ),
]
