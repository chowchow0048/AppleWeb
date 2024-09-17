from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.db.models import F
from django.forms import CheckboxSelectMultiple, ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget  # CKEditor 5 위젯 추가
import re

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


class MyAdminSite(admin.AdminSite):
    site_header = "애플과학 관리 시스템"
    site_title = "애플과학 관리자"
    site_name = "애플과학 관리 시스템"
    index_title = "관리자 대시보드"

    def has_permission(self, request):
        return request.user.is_active and request.user.is_superuser


admin_site = MyAdminSite(name="myadmin")


# UserAdmin 클래스 확장
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ("로그인 정보", {"fields": ("username", "password")}),
        (
            "회원 정보",
            {
                "fields": (
                    "name",
                    "phone",
                    "parent_phone",
                    "school",
                    "grade",
                    "courses",
                    "courses_count",
                )
            },
        ),
        (
            "권환 및 활성화",
            {
                "fields": (
                    "is_active",
                    "is_teacher",
                    "is_manager",
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
        # (
        #     "출석 및 결석",
        #     {"fields": ("attended_dates", "absent_dates")},
        # ),
        # (
        #     "강의",
        #     {"fields": "courses"},
        # ),
        ("로그인 기록 및 생성 일시", {"fields": ("last_login", "date_joined")}),
    )
    list_display = (
        "is_active",
        "name",
        "school",
        "grade",
        "courses_count",
        "payment_count",
        "id",
    )
    filter_horizontal = ("courses",)

    list_filter = (
        "is_active",
        "school",
        "grade",
        "is_teacher",
        "is_manager",
        "courses_count",
        "payment_count",
    )
    search_fields = (
        "username",
        "name",
    )
    actions = [
        "activate_users",
        "deactivate_users",
        "sync_payment_request",
        "sync_courses_count",
        "sync_courses",
        "format_phone_numbers",
        "set_payment_request_true",
        "set_payment_request_false",
        "sub_payment_count_1",
        "add_payment_count_1",
        "add_payment_count_4",
        "add_payment_count_8",
        "add_payment_count_12",
        "set_payment_count_1",
        "set_payment_count_4",
        "set_payment_count_8",
        "set_payment_count_12",
    ]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 사용자 업데이트 시 관련된 Course의 course_students 필드를 업데이트
        for course in obj.courses.all():
            if obj not in course.course_students.all():
                course.course_students.add(obj)
            course.save()

    def sync_payment_request(self, request, queryset):
        for user in queryset:
            if user.payment_count <= 0:
                user.payment_request = True
            else:
                user.payment_request = False
            user.save()

        self.message_user(request, "선택된 사용자들의 결제요청이 동기화 되었습니다.")

    sync_payment_request.short_description = "결제요청 동기화"

    def sync_courses(self, request, queryset):
        for user in queryset:
            # 현재 사용자가 등록된 활성화된 수업들 (course.is_active=True)
            user_courses = set(user.courses.filter(is_active=True))

            # 현재 사용자가 course_students에 포함된 활성화된 수업들
            correct_courses = set(
                Course.objects.filter(course_students=user, is_active=True)
            )

            # 활성화된 course_students에는 있지만 user의 courses에 없는 경우 추가
            for course in correct_courses - user_courses:
                user.courses.add(course)

            # user의 courses에 있지만 course_students에 없는 경우 제거 (비활성화된 수업 포함)
            for course in user.courses.all():
                if not course.is_active or course not in correct_courses:
                    user.courses.remove(course)

            user.save()

        self.message_user(request, "선택된 사용자들의 수업이 동기화되었습니다.")

    sync_courses.short_description = "수업 동기화"

    def sync_courses_count(self, request, queryset):
        for user in queryset:
            user.courses_count = user.courses.count()
            user.save()

        self.message_user(
            request, "선택된 사용자들의 선택과목 수 가 동기화 되었습니다."
        )

    sync_courses_count.short_description = "선택과목 수 동기화"

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, ("%d 활성화" % count))

    activate_users.short_description = "회원 활성화"

    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, ("%d 비활성화" % count))

    deactivate_users.short_description = "회원 비활성화"

    def format_phone_numbers(modeladmin, request, queryset):
        formatted_count = 0

        for user in queryset:
            # 전화번호에서 숫자 이외의 문자를 제거
            if user.phone:
                digits = re.sub(r"\D", "", user.phone)

                user.phone = f"{digits[:3]}-{digits[3:7]}-{digits[7:11]}"
                formatted_count += 1

            if user.parent_phone:
                parent_digits = re.sub(r"\D", "", user.parent_phone)

                user.parent_phone = (
                    f"{parent_digits[:3]}-{parent_digits[3:7]}-{parent_digits[7:11]}"
                )
                formatted_count += 1

            user.save()

        modeladmin.message_user(
            request,
            f"{formatted_count}명의 사용자의 전화번호가 형식에 맞게 수정되었습니다.",
        )

    format_phone_numbers.short_description = "전화번호 정규화"

    def set_payment_request_true(self, request, queryset):
        count = queryset.update(payment_request=True)
        self.message_user(request, ("%d 결제요청 ON" % count))

    set_payment_request_true.short_description = "결제요청 ON"

    def set_payment_request_false(self, request, queryset):
        count = queryset.update(payment_request=False)
        self.message_user(request, ("%d 결제요청 OFF" % count))

    set_payment_request_false.short_description = "결제요청 OFF"

    def sub_payment_count_1(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") - 1)
        self.message_user(request, ("%d 결제횟수 1회 감소" % count))

    sub_payment_count_1.short_description = "결제횟수 1회 감소"

    def add_payment_count_1(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 1)
        self.message_user(request, ("%d 결제횟수 1회 추가" % count))

    add_payment_count_1.short_description = "결제횟수 1회 추가"

    def add_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 4)
        self.message_user(request, ("%d 결제횟수 4회 추가" % count))

    add_payment_count_4.short_description = "결제횟수 4회 추가"

    def add_payment_count_8(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 8)
        self.message_user(request, ("%d 결제횟수 8회 추가" % count))

    add_payment_count_8.short_description = "결제횟수 8회 추가"

    def add_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=F("payment_count") + 12)
        self.message_user(request, ("%d 결제횟수 12회 추가" % count))

    add_payment_count_12.short_description = "결제횟수 12회 추가"

    def set_payment_count_1(self, request, queryset):
        count = queryset.update(payment_count=1)
        self.message_user(request, ("%d 결제횟수 1회로 변경" % count))

    set_payment_count_1.short_description = "결제횟수 1회로 변경"

    def set_payment_count_4(self, request, queryset):
        count = queryset.update(payment_count=4)
        self.message_user(request, ("%d 결제횟수 4회로 변경" % count))

    set_payment_count_4.short_description = "결제횟수 4회로 변경"

    def set_payment_count_8(self, request, queryset):
        count = queryset.update(payment_count=8)
        self.message_user(request, ("%d 결제횟수 8회로 변경" % count))

    set_payment_count_8.short_description = "결제횟수 8회로 변경"

    def set_payment_count_12(self, request, queryset):
        count = queryset.update(payment_count=12)
        self.message_user(request, ("%d 결제횟수 12회로 변경" % count))

    set_payment_count_12.short_description = "결제횟수 12회로 변경"

    # def set_physics_true(self, request, queryset):
    #     count = queryset.update(physics=True)
    #     self.message_user(request, ("%d 선택과목 물리 ON" % count))

    # set_physics_true.short_description = "선택과목 물리 ON"

    # def set_physics_false(self, request, queryset):
    #     count = queryset.update(physics=False)
    #     self.message_user(request, ("%d 선택과목 물리 OFF" % count))

    # set_physics_false.short_description = "선택과목 물리 OFF"

    # def set_chemistry_true(self, request, queryset):
    #     count = queryset.update(chemistry=True)
    #     self.message_user(request, ("%d 선택과목 화학 ON" % count))

    # set_chemistry_true.short_description = "선택과목 화학 ON"

    # def set_chemistry_false(self, request, queryset):
    #     count = queryset.update(chemistry=False)
    #     self.message_user(request, ("%d 선택과목 화학 OFF" % count))

    # set_chemistry_false.short_description = "선택과목 화학 OFF"

    # def set_biology_true(self, request, queryset):
    #     count = queryset.update(biology=True)
    #     self.message_user(request, ("%d 선택과목 생명과학 ON" % count))

    # set_biology_true.short_description = "선택과목 생명과학 ON"

    # def set_biology_false(self, request, queryset):
    #     count = queryset.update(biology=False)
    #     self.message_user(request, ("%d 선택과목 생명과학 OFF" % count))

    # set_biology_false.short_description = "선택과목 생명과학 OFF"

    # def set_earth_science_true(self, request, queryset):
    #     count = queryset.update(earth_science=True)
    #     self.message_user(request, ("%d 선택과목 지구과학 ON" % count))

    # set_earth_science_true.short_description = "선택과목 지구과학 ON"

    # def set_earth_science_false(self, request, queryset):
    #     count = queryset.update(earth_science=False)
    #     self.message_user(request, ("%d 선택과목 지구과학 OFF" % count))

    # set_earth_science_false.short_description = "선택과목 지구과학 OFF"

    # def set_integrated_science_true(self, request, queryset):
    #     count = queryset.update(integrated_science=True)
    #     self.message_user(request, ("%d 선택과목 통합과학 ON" % count))

    # set_integrated_science_true.short_description = "선택과목 통합과학 ON"

    # def set_integrated_science_false(self, request, queryset):
    #     count = queryset.update(integrated_science=False)
    #     self.message_user(request, ("%d 선택과목 통합과학 OFF" % count))

    # set_integrated_science_false.short_description = "선택과목 통합과학 OFF"


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
    actions = (
        "activate_course",
        "deactivate_course",
        "only_active_students",
        "set_day_wed",
        "set_day_thu",
        "set_day_fri",
        "set_day_sat",
        "set_day_sun",
        "set_time_1200",
    )
    filter_horizontal = ("course_students",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # 수업 업데이트 시 관련된 User의 courses 필드를 업데이트
        for student in obj.course_students.all():
            if obj not in student.courses.all():
                student.courses.add(obj)
            student.save()

    def activate_course(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, ("%d 강의 활성화" % count))

    activate_course.short_description = "강의 활성화"

    def deactivate_course(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, ("%d 강의 비활성화" % count))

    deactivate_course.short_description = "강의 비활성화"

    def only_active_students(self, request, queryset):
        for course in queryset:
            for student in course.course_students.all():
                if not student.is_active:
                    course.course_students.remove(student)

            course.save()

        self.message_user(request, "비활성 학생 삭제")

    only_active_students.short_description = "비활성 학생 삭제"

    def set_day_wed(self, request, queryset):
        count = queryset.update(course_day="수요일")
        self.message_user(request, ("%d 수업요일 == 수요일" % count))

    set_day_wed.short_description = "수업요일을 수요일로"

    def set_day_thu(self, request, queryset):
        count = queryset.update(course_day="목요일")
        self.message_user(request, ("%d 수업요일 == 목요일" % count))

    set_day_thu.short_description = "수업요일을 목요일로"

    def set_day_fri(self, request, queryset):
        count = queryset.update(course_day="금요일")
        self.message_user(request, ("%d 수업요일 == 금요일" % count))

    set_day_fri.short_description = "수업요일을 금요일로"

    def set_day_sat(self, request, queryset):
        count = queryset.update(course_day="토요일")
        self.message_user(request, ("%d 수업요일 == 토요일" % count))

    set_day_sat.short_description = "수업요일을 토요일로"

    def set_day_sun(self, request, queryset):
        count = queryset.update(course_day="일요일")
        self.message_user(request, ("%d 수업요일 == 일요일" % count))

    set_day_sun.short_description = "수업요일을 일요일로"

    def set_time_1200(self, request, queryset):
        count = queryset.update(course_time="12:00:00")
        self.message_user(request, ("%d 수업시간==1200" % count))

    set_time_1200.short_description = "수업시간 1200"


# AttendanceAdmin 클래스
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date")
    list_filter = ("course", "date")
    search_fields = ("student__username", "course__title")


class AbsenceAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "date")
    list_filter = ("course", "date")
    search_fields = ("student__username", "course__title")


class BoardAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Board
        fields = "__all__"


class BoardAdmin(admin.ModelAdmin):
    form = BoardAdminForm
    list_display = ("title", "author", "created_at", "updated_at")


class ReviewAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))

    class Meta:
        model = Review
        fields = "__all__"


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewAdminForm
    list_display = (
        "school",
        "name",
        "university",
        "major",
        "title",
        "created_at",
    )
    list_filter = ("school",)


# WaitlistAdmin 클래스
# class WaitlistAdmin(admin.ModelAdmin):
#     list_display = ("name", "school", "grade", "parent_phone", "note")
#     list_filter = ("school", "grade")
#     search_fields = ("name", "school")


# class BlacklistAdmin(admin.ModelAdmin):
#     list_display = ("name", "school", "grade", "parent_phone", "note")
#     list_filter = ("school", "grade")
#     search_fields = ("name", "school")


# 모델을 admin 사이트에 등록
admin.site.register(User, UserAdmin)
admin.site.register(Board)
admin.site.register(Review)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Absence, AbsenceAdmin)
# admin.site.register(Waitlist, WaitlistAdmin)
# admin.site.register(Blacklist, BlacklistAdmin)
