from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


class User(AbstractUser):
    LEVEL_CHOICES = (
        ("student", "학생"),
        ("teacher", "선생님"),
        ("staff", "직원"),
    )
    SCHOOL_CHOICES = (
        ("세화고", "세화고"),
        ("세화여고", "세화여고"),
        ("반포고", "반포고"),
        ("상문고", "상문고"),
        ("직접입력", "직접입력"),
    )
    GRADE_CHOICES = (
        ("1학년", "1학년"),
        ("2학년", "2학년"),
        ("3학년", "3학년"),
    )

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    school = models.CharField(
        max_length=50, choices=SCHOOL_CHOICES, blank=True, null=True
    )
    grade = models.CharField(
        max_length=10, choices=GRADE_CHOICES, blank=True, null=True
    )
    create_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 학생 레벨의 사용자는 school과 grade 필드를 반드시 입력해야 합니다.
        if self.level == "student" and (not self.school or not self.grade):
            raise ValidationError("학생 사용자는 학교와 학년을 입력해야 합니다.")
        super().clean()


class Board(models.Model):
    POSTED_IN_CHOICES = (("community", "커뮤니티"), ("main", "메인"))

    title = models.CharField(max_length=100, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="작성자"
    )
    posted_in = models.CharField(
        max_length=10,
        choices=POSTED_IN_CHOICES,
        default="community",
        verbose_name="종류",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성 날짜")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 날짜")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글들"


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
        max_length=10, choices=SCHOOL_CHOICES, verbose_name="고등학교"
    )
    name = models.CharField(max_length=10, verbose_name="학생 이름")
    # university = models.CharField(max_length=10, verbose_name="대학교")
    # major = models.CharField(max_length=20, verbose_name="학과")
    result = models.CharField(max_length=50, verbose_name="결과")
    content = models.TextField(max_length=1500, verbose_name="수강 후기")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="작성 시간")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "수강후기"
        # verbose_name.plural = "수강후기들"
