from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Profile
from apps.core.models import College, Department, Course, BusStop


class SignupForm(UserCreationForm):
    """ユーザー登録フォーム"""
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "メールアドレスを入力してください",
            "autofocus": True
        }),
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "パスワードを入力してください"
        }),
    )
    password2 = forms.CharField(
        label="パスワード（確認用）",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "もう一度パスワードを入力してください"
        }),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ["email", "password1", "password2"]
        labels = {
            "email": "メールアドレス",
            "password1": "パスワード",
            "password2": "パスワード（確認用）",
        }



class ProfileForm(forms.ModelForm):
    """プロフィール編集フォーム"""
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        required=False,
        label='カレッジ',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='学科',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label='コース／専攻',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )
    grade = forms.ChoiceField(
        choices=Profile.GRADE_CHOICES,
        required=False,
        label='学年',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )
    class_number = forms.ChoiceField(
        choices=Profile.CLASS_CHOICES,
        required=False,
        label='クラス',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )
    bus_stop = forms.ModelChoiceField(
        queryset=BusStop.objects.all(),
        required=False,
        label='バス',
        widget=forms.Select(attrs={
            "class": "form-select",
        })
    )


    class Meta:
        model = Profile
        fields = [
            'college',
            'department',
            'course',
            'grade',
            'class_number',
            'bus_stop',
        ]
        labels = {
            'college': 'カレッジ',
            'department': '学科',
            'course': 'コース／専攻',
            'grade': '学年',
            'class_number': 'クラス',
            'bus_stop': 'バス',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ChoiceField に「---------」を追加
        for field in ['grade', 'class_number']:
            self.fields[field].choices = [('', '---------')] + list(self.fields[field].choices)

        # ModelChoiceField の空ラベルを統一
        for field in ['college', 'department', 'course', 'bus_stop']:
            self.fields[field].empty_label = '---------'

        # 全て必須化
        for field in self.fields:
            self.fields[field].required = True



class CustomAuthenticationForm(AuthenticationForm):
    """ログインフォーム"""
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
