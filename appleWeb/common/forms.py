from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "name",
            "phone",
            "parent_phone",
            "school",
            "grade",
        ]
        labels = {
            "username": "아이디",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "name": "이름",
            "phone": "핸드폰 번호 (핸드폰 미소지 시 빈칸)",
            "parent_phone": "부모님 핸드폰 번호",
            "school": "학교",
            "grade": "학년",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "아이디"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "이름"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "핸드폰 번호"}
            ),
            "parent_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "부모님 핸드폰 번호"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # request.POST에서 직접 과목 필드를 읽어와서 처리합니다.
        user.integrated_science = self.data.get("integrated_science")
        user.physics = self.data.get("physics")
        user.chemistry = self.data.get("chemistry")
        user.biology = self.data.get("biology")
        user.earth_science = self.data.get("earth_science")

        if commit:
            user.save()
            self.save_m2m()
        return user

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호"}
        )
        self.fields["password1"].label = "비밀번호"
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "비밀번호 확인"}
        )
        self.fields["password2"].label = "비밀번호 확인"
        self.fields["school"].widget = forms.RadioSelect(
            attrs={"class": "radio-custom"}
        )
        self.fields["school"].choices = User.SCHOOL_CHOICES
        self.fields["grade"].widget = forms.RadioSelect(attrs={"class": "radio-custom"})
        self.fields["grade"].choices = User.GRADE_CHOICES

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) > 20:
            raise forms.ValidationError("사용자 이름은 최대 20글자까지 가능합니다.")

        UserModel = get_user_model()
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError("중복된 아이디 입니다.")

        return username

    # def clean_password1(self):
    #     password1 = self.cleaned_data.get("password1")
    #     if len(password1) < 8:
    #         raise forms.ValidationError("비밀번호는 최소 8글자 이상이어야 합니다.")
    #     return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone
        else:
            if not phone.isdigit():
                raise forms.ValidationError("전화번호는 숫자만 포함해야 합니다.")
        return phone

    def clean_parent_phone(self):
        parent_phone = self.cleaned_data.get("parent_phone")
        if not parent_phone.isdigit():
            raise forms.ValidationError("부모님 전화번호는 숫자만 포함해야 합니다.")
        return parent_phone

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        parent_phone = cleaned_data.get("parent_phone")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "두 비밀번호가 일치하지 않습니다.")
        return cleaned_data
