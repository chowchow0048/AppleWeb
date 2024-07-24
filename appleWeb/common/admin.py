from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.db.models import F
from django.forms import CheckboxSelectMultiple, ModelForm

from .models import (
    Absence,
    Attendance,
    Blacklist,
    Board,
    Course,
    Review,
    User,
    Waitlist,
)


# Custom AdminSite을 정의하여 superuser만 접근할 수 있도록 함
class MyAdminSite(admin.AdminSite):
    def has_permission(self, request):
        # superuser만 관리자 페이지에 접근할 수 있도록 설정
        return request.user.is_active and request.user.is_superuser


# 기존의 admin.site 인스턴스를 custom AdminSite 인스턴스로 대체
admin_site = MyAdminSite(name="myadmin")


# UserAdmin 클래스 확장
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "회원 정보",
            {"fields": ("name", "phone", "parent_phone", "school", "grade", "courses")},
        ),
        (
            "권환 및 활성화",
            {
                "fields": (
                    "is_active",
                    "is_teacher",
                    "is_manager",
                    # "is_staff",
                    # "is_superuser",
                    # "groups",
                    # "user_permissions",
                )
            },
        ),
        (
            "결제 정보",
            {
                "fields": (
                    "payment_count",
                    "payment_request",
                )
            },
        ),
        (
            "선택과목",
            {
                "fields": (
                    "physics",
                    "chemistry",
                    "biology",
                    "earth_science",
                    "integrated_science",
                )
            },
        ),
        (
            "출석 및 결석",
            {"fields": ("attended_dates", "absent_dates")},
        ),
        # (
        #     "강의",
        #     {"fields": "courses"},
        # ),
        ("로그인 기록 및 생성 일시", {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "is_active",
        "name",
        "is_teacher",
        "is_manager",
        "school",
        "grade",
    )
    list_filter = (
        "is_active",
        "school",
        "grade",
        "is_teacher",
        "is_manager",
        # "physics",
        # "chemistry",
        # "biology",
        # "earth_science",
    )
    search_fields = (
        "username",
        "name",
    )
    actions = [
        "activate_users",
        "deactivate_users",
        "set_payment_request_true",
        "set_payment_request_false",
        "add_payment_count_12",
        "set_payment_count_12",
        "add_payment_count_4",
        "set_payment_count_4",
        "set_payment_count_1",
        "set_physics_true",
        "set_physics_false",
        "set_chemistry_true",
        "set_chemistry_false",
        "set_biology_true",
        "set_biology_false",
        "set_earth_science_true",
        "set_earth_science_false",
        "set_integrated_science_true",
        "set_integrated_science_false",
    ]

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, ("%d 활성화" % count))

    activate_users.short_description = "회원 활성화"

    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, ("%d 비활성화" % count))

    deactivate_users.short_description = "회원 비활성화"

    def set_payment_request_true(self, request, queryset):
        count = queryset.update(payment_request=True)
        self.message_user(request, ("%d 결제요청 ON" % count))

    set_payment_request_true.short_description = "결제요청 ON"

    def set_payment_request_false(self, request, queryset):
        count = queryset.update(payment_request=False)
        self.message_user(request, ("%d 결제요청 OFF" % count))

    set_payment_request_false.short_description = "결제요청 OFF"

    def add_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 12)
        self.message_user(request, ("%d 결제횟수 12회 추가" % count))

    add_payment_count_12.short_description = "결제횟수 12회 추가"

    def set_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=12)
        self.message_user(request, ("%d 결제횟수 12회로 변경" % count))

    set_payment_count_12.short_description = "결제횟수 12회로 변경"

    def add_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 4)
        self.message_user(request, ("%d 결제횟수 4회 추가" % count))

    add_payment_count_4.short_description = "결제횟수 4회 추가"

    def set_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=4)
        self.message_user(request, ("%d 결제횟수 4회로 변경" % count))

    set_payment_count_4.short_description = "결제횟수 4회로 변경"

    def set_payment_count_1(self, request, queryset):
        count = queryset.update(payment_count=1)
        self.message_user(request, ("%d 결제횟수 1회로 변경" % count))

    set_payment_count_1.short_description = "결제횟수 1회로 변경"

    def set_physics_true(self, request, queryset):
        count = queryset.update(physics=True)
        self.message_user(request, ("%d 선택과목 물리 ON" % count))

    set_physics_true.short_description = "선택과목 물리 ON"

    def set_physics_false(self, request, queryset):
        count = queryset.update(physics=False)
        self.message_user(request, ("%d 선택과목 물리 OFF" % count))

    set_physics_false.short_description = "선택과목 물리 OFF"

    def set_chemistry_true(self, request, queryset):
        count = queryset.update(chemistry=True)
        self.message_user(request, ("%d 선택과목 화학 ON" % count))

    set_chemistry_true.short_description = "선택과목 화학 ON"

    def set_chemistry_false(self, request, queryset):
        count = queryset.update(chemistry=False)
        self.message_user(request, ("%d 선택과목 화학 OFF" % count))

    set_chemistry_false.short_description = "선택과목 화학 OFF"

    def set_biology_true(self, request, queryset):
        count = queryset.update(biology=True)
        self.message_user(request, ("%d 선택과목 생명과학 ON" % count))

    set_biology_true.short_description = "선택과목 생명과학 ON"

    def set_biology_false(self, request, queryset):
        count = queryset.update(biology=False)
        self.message_user(request, ("%d 선택과목 생명과학 OFF" % count))

    set_biology_false.short_description = "선택과목 생명과학 OFF"

    def set_earth_science_true(self, request, queryset):
        count = queryset.update(earth_science=True)
        self.message_user(request, ("%d 선택과목 지구과학 ON" % count))

    set_earth_science_true.short_description = "선택과목 지구과학 ON"

    def set_earth_science_false(self, request, queryset):
        count = queryset.update(earth_science=False)
        self.message_user(request, ("%d 선택과목 지구과학 OFF" % count))

    set_earth_science_false.short_description = "선택과목 지구과학 OFF"

    def set_integrated_science_true(self, request, queryset):
        count = queryset.update(integrated_science=True)
        self.message_user(request, ("%d 선택과목 통합과학 ON" % count))

    set_integrated_science_true.short_description = "선택과목 통합과학 ON"

    def set_integrated_science_false(self, request, queryset):
        count = queryset.update(integrated_science=False)
        self.message_user(request, ("%d 선택과목 통합과학 OFF" % count))

    set_integrated_science_false.short_description = "선택과목 통합과학 OFF"


class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        # course_teacher 필드에 대한 쿼리셋 수정
        self.fields["course_teacher"].queryset = User.objects.filter(is_teacher=True)
        # course_students 필드에 대한 쿼리셋 수정
        self.fields["course_students"].queryset = User.objects.filter(
            is_teacher=False, is_manager=False
        )


# CourseAdmin 클래스
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "course_school",
                    "course_grade",
                    "course_subject",
                    "course_day",
                    "course_time",
                    "course_room",
                    "course_teacher",
                    "course_students",
                )
            },
        ),
    )
    list_display = (
        "id",
        "is_active",
        "course_school",
        "course_grade",
        "course_subject",
        "course_day",
        "course_time",
        "course_room",
        "course_teacher",
    )
    list_filter = (
        "is_active",
        "course_school",
        "course_grade",
        "course_subject",
        "course_day",
    )
    actions = ("activate_course", "deactivate_course")
    filter_horizontal = ("course_students",)

    def activate_course(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, ("%d 강의 활성화" % count))

    activate_course.short_description = "강의 활성화"

    def deactivate_course(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, ("%d 강의 비활성화" % count))

    deactivate_course.short_description = "강의 비활성화"


# AttendanceAdmin 클래스
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date")
    list_filter = ("course", "student")
    search_fields = ("student__username", "course__title")


class AbsenceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date")
    list_filter = ("course", "student")
    search_fields = ("student__username", "course__title")


# WaitlistAdmin 클래스
class WaitlistAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "grade", "parent_phone", "note")
    list_filter = ("school", "grade")
    search_fields = ("name", "school")


class BlacklistAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "grade", "parent_phone", "note")
    list_filter = ("school", "grade")
    search_fields = ("name", "school")


# 모델을 admin 사이트에 등록
admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Review)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Waitlist, WaitlistAdmin)
admin.site.register(Blacklist, BlacklistAdmin)
