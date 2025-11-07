from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, College, Department, Course


class SignupForm(UserCreationForm):
    """ユーザー登録フォーム"""

    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        required=False,
        label='学部'
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='学科'
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label='コース／専攻'
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'grade',
            'college',
            'department',
            'course',
        ]

class CustomAuthenticationForm(AuthenticationForm):
    """ログインフォーム（ユーザー名またはメールアドレス）"""

    username = forms.CharField(
        label='ユーザー名',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput()
    )
