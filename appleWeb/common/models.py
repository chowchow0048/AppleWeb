from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from django_ckeditor_5.fields import CKEditor5Field  # CKEditor 5 필드 추가
import logging

logger_appleWeb = logging.getLogger("appleWeb")


class User(AbstractUser):
    GRADE_CHOICES = (
        ("에비고1", "예비고1"),
        ("1학년", "1학년"),
        ("2학년", "2학년"),
        ("3학년", "3학년"),
    )
    SCHOOL_CHOICES = (
        ("세화고", "세화고"),
        ("세화여고", "세화여고"),
        ("연합반", "연합반"),
    )

    name = models.CharField(max_length=100, null=False, verbose_name="이름")
    phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="전화번호"
    )
    parent_phone = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="부모님 전화번호"
    )
    is_teacher = models.BooleanField(default=False, verbose_name="강사")
    is_manager = models.BooleanField(default=False, verbose_name="행정")
    school = models.CharField(
        max_length=50,
        choices=SCHOOL_CHOICES,
        blank=True,
        null=True,
        verbose_name="학교",
    )
    grade = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES,
        blank=True,
        null=True,
        verbose_name="학년",
    )
    physics = models.BooleanField(default=False, verbose_name="물리")
    chemistry = models.BooleanField(default=False, verbose_name="화학")
    biology = models.BooleanField(default=False, verbose_name="생명과학")
    earth_science = models.BooleanField(default=False, verbose_name="지구과학")
    integrated_science = models.BooleanField(default=False, verbose_name="통합과학")
    courses = models.ManyToManyField(
        "Course",
        related_name="enrolled_students",
        blank=True,
        verbose_name="수업 시간표",
    )
    courses_count = models.IntegerField(default=0, verbose_name="선택과목수")
    payment_count = models.IntegerField(default=12, verbose_name="결제 횟수")
    payment_request = models.BooleanField(default=False, verbose_name="결제 요청")

    latest_payment = models.DateField(
        blank=True, null=True, verbose_name="최근 결제 날짜"
    )
    is_active = models.BooleanField(
        default=False, verbose_name="활성화"
    )  # 관리자 승인 전까지는 비활성화된 계정 처리
    attended_dates = models.ManyToManyField(
        "Attendance",
        related_name="attended_at",
        blank=True,
        verbose_name="출석 날짜",
    )
    absent_dates = models.ManyToManyField(
        "Absence",
        related_name="absent_at",
        blank=True,
        verbose_name="결석 날짜",
    )

    def __str__(self):
        if self.is_teacher:
            return f"{self.name}"
        if self.is_manager:
            return f"{self.name}"
        else:
            return f"{self.school} {self.grade} {self.name}"

    class Meta:
        verbose_name = "회원"
        verbose_name_plural = "회원"


class Course(models.Model):
    DAY_CHOICES = (
        ("월요일", "월요일"),
        ("화요일", "화요일"),
        ("수요일", "수요일"),
        ("목요일", "목요일"),
        ("금요일", "금요일"),
        ("토요일", "토요일"),
        ("일요일", "일요일"),
    )
    ROOM_CHOICES = (
        ("402", "402"),
        ("403", "403"),
        ("404", "404"),
        ("408", "408"),
        ("409", "409"),
        ("415", "415"),
    )
    SUBJECT_CHOICES = (
        ("physics", "물리"),
        ("chemistry", "화학"),
        ("biology", "생명과학"),
        ("earth_science", "지구과학"),
        ("integrated_science", "통합과학"),
    )
    is_active = models.BooleanField(
        default=False, verbose_name="활성화"
    )  # 관리자 승인 전까지는 비활성화된 계정 처리
    course_school = models.CharField(
        max_length=50, choices=User.SCHOOL_CHOICES, verbose_name="학교"
    )
    course_grade = models.CharField(
        max_length=10, choices=User.GRADE_CHOICES, verbose_name="학년"
    )
    course_subject = models.CharField(
        max_length=30,
        choices=SUBJECT_CHOICES,
        default="선택과목",
        verbose_name="선택과목",
    )
    course_day = models.CharField(
        max_length=10, choices=DAY_CHOICES, verbose_name="수업 요일", default="일요일"
    )
    course_time = models.TimeField(verbose_name="수업 시작 시간", default="10:00")
    course_room = models.CharField(
        max_length=10,
        choices=ROOM_CHOICES,
        blank=True,
        null=True,
        verbose_name="강의실",
    )
    course_teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="taught_courses",
        verbose_name="선생",
    )
    course_students = models.ManyToManyField(
        User,
        related_name="enrolled_courses",
        blank=True,
        verbose_name="학생",
    )

    def get_next_class_time(self, from_time=None):
        try:
            if from_time is None:
                from_time = timezone.now()

            day_to_number = {
                "월요일": 0,
                "화요일": 1,
                "수요일": 2,
                "목요일": 3,
                "금요일": 4,
                "토요일": 5,
                "일요일": 6,
            }
            course_day_number = day_to_number.get(self.course_day)
            if course_day_number is None:
                raise ValueError(f"Invalid course_day: {self.course_day}")

            current_day_number = from_time.weekday()

            days_ahead = course_day_number - current_day_number
            if days_ahead <= 0:
                days_ahead += 7

            next_date = from_time.date() + timedelta(days=days_ahead)
            next_time = timezone.make_aware(
                datetime.combine(next_date, self.course_time)
            )

            if next_time <= from_time:
                next_time += timedelta(days=7)

            # print(
            #     "course:",
            #     course_day_number,
            #     "today:",
            #     current_day_number,
            #     "course:",
            #     days_ahead,
            #     next_date,
            #     next_time,
            # )

            return next_time
        except Exception as e:
            logger_appleWeb.error(
                f"Error in get_next_class_time for course {self.id}: {str(e)}"
            )
            return None

    def __str__(self):
        subject = self.course_subject

        if subject == "physics":
            subject = "물리"
        elif subject == "chemistry":
            subject = "화학"
        elif subject == "biology":
            subject = "생명과학"
        elif subject == "earth_science":
            subject = "지구과학"
        else:
            subject = "통합과학"

        return f"{self.course_school} {self.course_grade} {subject} {self.course_day} {self.course_time}"

    class Meta:
        verbose_name = "수업"
        verbose_name_plural = "수업"


class Handover(models.Model):
    SHIFT_CHOICES = (("오전", "오전"), ("오후", "오후"))
    shift = models.CharField(
        max_length=5, verbose_name="제목-시간", choices=SHIFT_CHOICES, default="오전"
    )
    content = CKEditor5Field("내용", config_name="default")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="작성자",
        default=1,
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="작성날짜"
    )  # DateTimeField로 수정

    def __str__(self):
        return f"{self.created_date} {self.shift} - {self.author}"

    class Meta:
        verbose_name = "인수인계"
        verbose_name_plural = "인수인계"


class Attendance(models.Model):
    student = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name="학생",
        related_name="attended_student",
    )
    date = models.DateField(verbose_name="출석 날짜")
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="수업",
        related_name="attendances",
    )

    def __str__(self):
        # 출석 날짜와 연결된 수업 정보를 문자열로 반환
        return f"{self.student} - {self.course} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "출석"
        verbose_name_plural = "출석"
        ordering = ["date"]


class Absence(models.Model):
    student = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name="학생",
        related_name="absent_student",
    )
    date = models.DateField(verbose_name="결석 날짜")
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="수업",
        related_name="absent",
    )

    def __str__(self):
        # 출석 날짜와 연결된 수업 정보를 문자열로 반환
        return f"{self.student} - {self.course} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "결석"
        verbose_name_plural = "결석"
        ordering = ["date"]


class Waitlist(models.Model):
    school = models.CharField(
        max_length=10, choices=User.SCHOOL_CHOICES, verbose_name="학교"
    )
    grade = models.CharField(
        max_length=10, choices=User.GRADE_CHOICES, verbose_name="학년"
    )
    name = models.CharField(max_length=20, verbose_name="이름")
    phone = models.CharField(max_length=20, verbose_name="연락처", blank=True)
    note = CKEditor5Field("비고", config_name="default")
    date = models.DateField(auto_now_add=True, verbose_name="대기등록 날짜")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="등록한 관리자",
        related_name="waitlists",
        default=1,
    )

    def __str__(self):
        return f"대기: {self.school} {self.grade} - {self.name}"

    class Meta:
        ordering = ["-date"]
        verbose_name = "대기리스트"
        verbose_name_plural = "대기리스트"


class Blacklist(models.Model):
    school = models.CharField(
        max_length=10, choices=User.SCHOOL_CHOICES, verbose_name="학교"
    )
    grade = models.CharField(
        max_length=10, choices=User.GRADE_CHOICES, verbose_name="학년"
    )
    name = models.CharField(max_length=20, verbose_name="이름")
    phone = models.CharField(max_length=20, verbose_name="연락처", blank=True)
    note = CKEditor5Field("비고", config_name="default")
    date = models.DateField(auto_now_add=True, verbose_name="대기등록 날짜")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="등록한 관리자",
        related_name="blacklists",
        default=1,
    )

    def __str__(self):
        return f"블랙리스트: {self.school} {self.grade} - {self.name}"

    class Meta:
        ordering = ["-date"]
        verbose_name = "블랙리스트"
        verbose_name_plural = "블랙리스트"


class Board(models.Model):
    POSTED_IN_CHOICES = (
        ("community", "커뮤니티"),
        ("main", "메인"),
        ("management", "행정"),
    )

    title = models.CharField(max_length=100, verbose_name="제목")
    content = CKEditor5Field("내용", config_name="default")  # CKEditor 5 필드로 변경
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자"
    )
    posted_in = models.CharField(
        max_length=10,
        choices=POSTED_IN_CHOICES,
        default="main",
        verbose_name="종류",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성 날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 날짜")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "게시판"
        verbose_name_plural = "게시판"


class Review(models.Model):
    SCHOOL_CHOICES = (
        ("세화고", "세화고"),
        ("세화여고", "세화여고"),
        ("반포고", "반포고"),
        ("상문고", "상문고"),
        ("서울고", "서울고"),
        ("서문여고", "서문여고"),
        ("영동고", "영동고"),
    )

    school = models.CharField(
        max_length=10,
        choices=SCHOOL_CHOICES,
        verbose_name="고등학교",
        default="세화고",
    )
    name = models.CharField(max_length=10, verbose_name="학생 이름")
    university = models.CharField(
        max_length=20, verbose_name="대학교", default="Unknown"
    )
    major = models.CharField(max_length=20, verbose_name="학과", default="Unknown")
    title = models.CharField(
        max_length=100, verbose_name="제목", default="애플과학 수강후기"
    )
    content = CKEditor5Field("내용", config_name="default")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="작성 시간")
    image = models.ImageField(
        upload_to="review_images/", null=True, blank=True, verbose_name="이미지"
    )
    importance = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "수강후기"
        verbose_name_plural = "수강후기"
