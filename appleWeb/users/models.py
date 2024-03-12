from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


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
