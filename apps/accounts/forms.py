from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Faculty, Department, Course


class CustomUserCreationForm(UserCreationForm):
    """ユーザー登録フォーム（新規登録用）"""

    # 学部・学科・コースを選択肢として追加
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
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
        label='コース'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'grade',
            'faculty',
            'department',
            'course',
        ]
        labels = {
            'username': '名前',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（確認）',
            'grade': '学年',
            'faculty': '学部',
            'department': '学科',
            'course': 'コース',
        }
        help_texts = {field: '' for field in fields}


    # 🔽 ここを追加：メールアドレスのドメイン制限
    def clean_email(self):
        email = self.cleaned_data.get('email')
        required_domain = '@g.neec.ac.jp'

        if not email or not email.lower().endswith(required_domain):
            raise ValidationError(f'登録には {required_domain} のメールアドレスが必要です。')

        return email


class CustomAuthenticationForm(AuthenticationForm):
    """ログインフォーム（ユーザー名またはメールアドレス）"""

    username = forms.CharField(
        label='ユーザー名またはメールアドレス',
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput()
    )
