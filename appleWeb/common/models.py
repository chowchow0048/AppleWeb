from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    GRADE_CHOICES = (
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
    payment_count = models.IntegerField(default=12, verbose_name="결제 횟수")
    payment_request = models.BooleanField(default=False, verbose_name="결제 요청")
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

    # def clean(self):
    #     super().clean()
    #     # '1학년'인 경우 통합과학 외 다른 과목 선택 불가
    #     if self.grade == "1학년":
    #         print(
    #             "grade == 1:",
    #             self.integrated_science,
    #             self.physics,
    #             self.chemistry,
    #             self.biology,
    #             self.earth_science,
    #         )
    #         if not self.integrated_science or any(
    #             [self.physics, self.chemistry, self.biology, self.earth_science]
    #         ):
    #             raise ValidationError("1학년은 통합과학만 선택 가능합니다.")
    #     # '2학년'과 '3학년'인 경우 세 과목을 선택해야 함
    #     elif self.grade in ["2학년", "3학년"]:
    #         print(
    #             "grade != 1:",
    #             self.integrated_science,
    #             self.physics,
    #             self.chemistry,
    #             self.biology,
    #             self.earth_science,
    #         )
    #         selected_subjects = [
    #             self.physics,
    #             self.chemistry,
    #             self.biology,
    #             self.earth_science,
    #         ]
    #         if selected_subjects.count(True) != 3:
    #             raise ValidationError(
    #                 "2학년 및 3학년은 정확히 세 과목을 선택해야 합니다."
    #             )


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
    course_school = models.CharField(
        max_length=50, choices=User.SCHOOL_CHOICES, verbose_name="학교"
    )
    course_grade = models.CharField(
        max_length=10, choices=User.GRADE_CHOICES, verbose_name="학년"
    )
    # course_physics = models.BooleanField(default=False, verbose_name="물리")
    # course_chemistry = models.BooleanField(default=False, verbose_name="화학")
    # course_biology = models.BooleanField(default=False, verbose_name="생명과학")
    # course_earth_science = models.BooleanField(default=False, verbose_name="지구과학")
    # course_integrated_science = models.BooleanField(
    #     default=False, verbose_name="통합과학"
    # )
    course_subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        default="선택과목",
        verbose_name="선택과목",
    )
    course_day = models.CharField(
        max_length=10, choices=DAY_CHOICES, verbose_name="수업 요일"
    )
    course_time = models.TimeField(verbose_name="수업 시작 시간")
    course_room = models.CharField(
        max_length=10, choices=ROOM_CHOICES, null=True, verbose_name="강의실"
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

    # def clean(self):
    #     # 과목 필드의 상태를 검사
    #     subject_fields = [
    #         self.course_physics,
    #         self.course_chemistry,
    #         self.course_biology,
    #         self.course_earth_science,
    #         self.course_integrated_science,
    #     ]
    #     if subject_fields.count(True) != 1:
    #         raise ValidationError("정확히 하나의 과목만 True로 설정해야 합니다.")

    def __str__(self):
        # subject_names = []
        # if self.course_physics:
        #     subject_names.append("물리")
        # if self.course_chemistry:
        #     subject_names.append("화학")
        # if self.course_biology:
        #     subject_names.append("생명과학")
        # if self.course_earth_science:
        #     subject_names.append("지구과학")
        # if self.course_integrated_science:
        #     subject_names.append("통합과학")
        # subjects = ", ".join(subject_names)
        return f"{self.course_school} {self.course_grade} - {self.course_subject} {self.course_time}"

    class Meta:
        verbose_name = "수업"
        verbose_name_plural = "수업"


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
    parent_phone = models.CharField(max_length=20, verbose_name="부모님 전화번호")
    note = models.TextField(max_length=500, verbose_name="비고")
    applying_date = models.DateField(auto_now_add=True, verbose_name="대기등록 날짜")

    def __str__(self):
        return f"대기: {self.school} {self.grade} - {self.name}"


class Blacklist(models.Model):
    school = models.CharField(
        max_length=10, choices=User.SCHOOL_CHOICES, verbose_name="학교"
    )
    grade = models.CharField(
        max_length=10, choices=User.GRADE_CHOICES, verbose_name="학년"
    )
    name = models.CharField(max_length=20, verbose_name="이름")
    parent_phone = models.CharField(max_length=20, verbose_name="부모님 전화번호")
    note = models.TextField(max_length=500, verbose_name="비고")
    applying_date = models.DateField(auto_now_add=True, verbose_name="대기등록 날짜")

    def __str__(self):
        return f"블랙리스트: {self.school} {self.grade} - {self.name}"


class Board(models.Model):
    POSTED_IN_CHOICES = (
        ("community", "커뮤니티"),
        ("main", "메인"),
        ("management", "행정"),
    )

    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
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
    content = models.TextField(max_length=1500, verbose_name="수강 후기")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="작성 시간")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "수강후기"
        verbose_name_plural = "수강후기"
