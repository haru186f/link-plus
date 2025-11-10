from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
            'email',
            'password1',
            'password2',
            'college',
            'department',
            'course',
            'grade',
        ]
        labels = {
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード(確認用)',
            'college': 'カレッジ',
            'department': '学科',
            'course': 'コース／専攻',
            'grade': '学年',
        }



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "メールアドレスを入力してください",
            "autofocus": True
        }),
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "パスワードを入力してください"
        }),
    )
