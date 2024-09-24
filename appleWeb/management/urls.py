from django.urls import path
from . import views

urlpatterns = [
    path("", views.management_home, name="management_home"),  # 데일리 페이지
    path(  # 학생명단 페이지
        "student-list/", views.management_studentlist, name="management_studentlist"
    ),
    path(  # 출석부 페이지
        "lecture/<int:course_id>/",
        views.management_lecture,
        name="management_lecture",
    ),
    path(  # 행정 일지
        "manage-journal/",
        views.management_manage_journal,
        name="management_manage_journal",
    ),
    path(  # 학생 상세정보 페이지
        "student_detail/<int:student_id>/",
        views.management_student_detail,
        name="management_student_detail",
    ),
    path(  # 결제요청 페이지
        "pay-list/", views.management_paylist, name="management_paylist"
    ),
    # path(  # 특강 페이지
    #     "special-lecture/",
    #     views.management_special_lecture,
    #     name="management_special_lecture",
    # ),
    path(  # 대기명단 페이지 (작업중?)
        "wait-list/", views.management_waitList, name="management_waitlist"
    ),
    path(  # 블랙리스트 페이지 (작업중?)
        "black-list/", views.management_blacklist, name="management_blacklist"
    ),
    path(  # 출석부 상세 페이지 출결처리 api
        "bulk_attendance/", views.bulk_attendance, name="bulk_attendance"
    ),
    path(  # 데일리 페이지 수업 불러오기 api
        "api/courses/", views.api_courses, name="api_courses"
    ),
    path("api/students/", views.api_students, name="api_students"),  # 학생 명단 api
    # path(  # 특강 명단 api
    #     "api/special-lecture-students/",
    #     views.api_special_lecture_students,
    #     name="api_special_lecture_students",
    # ),
    # path(
    #     "record-special-lecture-attendance/",
    #     views.record_special_lecture_attendance,
    #     name="record_special_lecture_attendance",
    # ),
    path(  # 결제 요청 api
        "confirm-payment/<int:user_id>/", views.confirm_payment, name="confirm_payment"
    ),
    path(  # 출석부 상세 페이지 출력 api
        "export_attendance/<int:course_id>/",
        views.export_attendance_to_excel,
        name="export_attendance",
    ),
    # depricated
    # path("api/record_attendance/", views.record_attendance, name="record_attendance"),
    # path("api/record_absence/", views.record_absence, name="record_absence"),
    # path("notice", views.management_notice, name="management_notice"),
]
