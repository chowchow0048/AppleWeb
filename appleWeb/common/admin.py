from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from django.db.models import F
from .models import (
    User,
    Board,
    Review,
    Course,
    Attendance,
    Absence,
    Waitlist,
    Blacklist,
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
        "add_payment_count_12",
        "set_payment_count_12",
        "add_payment_count_4",
        "set_payment_count_4",
        "set_payment_count_1",
    ]

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(
            request, ("%d users have been successfully activated." % count)
        )

    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(
            request, ("%d users have been successfully deactivated." % count)
        )

    deactivate_users.short_description = "Deactivate selected users"

    def add_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 12)
        self.message_user(request, ("%d users' payment count increased by 12" % count))

    add_payment_count_12.short_description = (
        "Increase payment count by 12 for selected users"
    )

    def set_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=12)
        self.message_user(request, ("%d users' payment count increased by 12" % count))

    set_payment_count_12.short_description = (
        "Set payment count by 12 for selected users"
    )

    def add_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 4)
        self.message_user(request, ("%d users' payment count increased by 4" % count))

    add_payment_count_4.short_description = (
        "Increase payment count by 4 for selected users"
    )

    def set_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=4)
        self.message_user(request, ("%d users' payment count increased by 4" % count))

    set_payment_count_4.short_description = "Set payment count by 4 for selected users"

    def set_payment_count_1(self, request, queryset):
        count = queryset.update(payment_count=1)
        self.message_user(request, ("%d users payment_count set to 1" % count))

    set_payment_count_1.short_description = "Set payment count 1 for selected users"


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
    list_display = (
        "course_school",
        "course_grade",
        "course_subject",
        "course_day",
        "course_time",
        "course_room",
        "course_teacher",
    )
    list_filter = ("course_school", "course_grade", "course_subject", "course_day")
    fieldsets = (
        (
            None,
            {
                "fields": (
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
        # (
        #     "수강 과목",
        #     {
        #         "fields": (
        #             "course_physics",
        #             "course_chemistry",
        #             "course_biology",
        #             "course_earth_science",
        #             "course_integrated_science",
        #         )
        #     },
        # ),
    )
    filter_horizontal = ("course_students",)


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
