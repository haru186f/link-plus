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
            "placeholder": "もう一度パスワードを入力してくださいい"
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
            "placeholder": "カレッジを選択してください"
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label='学科',
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "学科を選択してください"
        })
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label='コース／専攻',
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "コース／専攻を選択してください"
        })
    )
    grade = forms.ChoiceField(
        choices=Profile.GRADE_CHOICES,
        required=False,
        label='学年',
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "学年を選択してください"
        })
    )
    class_number = forms.ChoiceField(
        choices=Profile.CLASS_CHOICES,
        required=False,
        label='クラス',
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "クラスを選択してください"
        })
    )
    bus_stop = forms.ModelChoiceField(
        queryset=BusStop.objects.all(),
        required=False,
        label='スクールバス',
        widget=forms.Select(attrs={
            "class": "form-select",
            "placeholder": "スクールバスを選択してください"
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
            'bus_stop': 'スクールバス',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔹 先頭に "---------" を必ず入れる（最良の方法）
        self.fields['grade'].choices = [('', '---------')] + list(self.fields['grade'].choices)
        self.fields['class_number'].choices = [('', '---------')] + list(self.fields['class_number'].choices)



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
