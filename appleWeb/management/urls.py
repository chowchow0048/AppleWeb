from django.urls import path
from . import views

urlpatterns = [
    path("", views.management_home, name="management_home"),  # 데일리 페이지
    path(  # 학생명단 페이지
        "studentlist/", views.management_studentlist, name="management_studentlist"
    ),
    path(  # 출석부 페이지
        "lecture/<int:course_id>/",
        views.management_lecture,
        name="management_lecture",
    ),
    path(  # 인수인계 페이지
        "handover/",
        views.management_handover,
        name="management_handover",
    ),
    # path(  # 인수인계 검색 api
    #     "handover/search/", views.search_handover, name="search_handover"
    # ),
    path(  # 인수인계 작성 페이지
        "handover/add/",
        views.management_handover_add,
        name="management_handover_add",
    ),
    path(  # 인수인계 상세 페이지
        "handover/<int:handover_id>/",
        views.management_handover_detail,
        name="management_handover_detail",
    ),
    path(
        "handover/update/<int:handover_id>/",
        views.management_handover_update,
        name="management_handover_update",
    ),
    path(
        "handover/delete/<int:handover_id>/",
        views.management_handover_delete,
        name="management_handover_delete",
    ),
    path(  # 학생 상세정보 페이지
        "student-detail/<int:student_id>/",
        views.management_student_detail,
        name="management_student_detail",
    ),
    path(  # 필터 및 검색 요청을 처리하는 뷰
        "paylist/fetch/", views.fetch_paylist, name="fetch_paylist"
    ),
    path(  # 필터 및 검색
        "confirm-payment/<int:user_id>/",
        views.confirm_payment,
        name="confirm_payment",
    ),
    path("paylist/", views.management_paylist, name="management_paylist"),
    path(  # 대기&블랙 페이지
        "wait-blacklist/",
        views.management_wait_black_list,
        name="management_wait_black_list",
    ),
    path(  # 대기&블랙 페이지 fetch api
        "wait-blacklist/fetch/",
        views.fetch_wait_black_list,
        name="fetch_wait_black_list",
    ),
    path(  # 대기블랙 명단 추가
        "wait-blacklist/add/",
        views.management_wait_black_list_add,
        name="management_wait_black_list_add",
    ),
    path(  # 대기블랙 명단 삭제
        "wait-blacklist/delete/<str:list_type>/<int:entry_id>/",
        views.management_wait_black_list_delete,
        name="management_wait_black_list_delete",
    ),
    path(  # 대기 명단 상세
        "wait-blacklist/wait-detail/<int:waitlist_id>/",
        views.management_wait_black_list_wait_detail,
        name="management_wait_black_list_wait_detail",
    ),
    path(  # 블랙 명단 상세
        "wait-blacklist/black-detail/<int:blacklist_id>/",
        views.management_wait_black_list_black_detail,
        name="management_wait_black_list_black_detail",
    ),
    path(  # 출석부 상세 페이지 출결처리 api
        "bulk-attendance/", views.bulk_attendance, name="bulk_attendance"
    ),
    path(  # 데일리 페이지 수업 불러오기 api
        "api/courses/", views.api_courses, name="api_courses"
    ),
    path("api/students/", views.api_students, name="api_students"),  # 학생 명단 api
    path(  # 결제 요청 api
        "confirm-payment/<int:user_id>/", views.confirm_payment, name="confirm_payment"
    ),
    path(  # 출석부 상세 페이지 출력 api
        "export_attendance/<int:course_id>/",
        views.export_attendance_to_excel,
        name="export_attendance",
    ),
]
