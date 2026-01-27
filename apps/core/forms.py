from django import forms
from django.contrib.auth import get_user_model
from .models import ReceivedEmail
from apps.core.models import (
    Department,
    LectureSchedule,
    SchoolPeriod,
    Room,
    Event,
)
from apps.accounts.models import Profile


class NewsForm(forms.ModelForm):
    class Meta:
        model = ReceivedEmail
        fields = ['target_department', 'target_grade', 'subject', 'body']

        labels = {
            'target_department': '投稿対象（未選択なら全員）',
            'subject': '件名',
            'body': '本文',
        }
        widgets = {
            'target_department': forms.Select(attrs={'class': 'form-select', 'id': 'id_target_department'}),
            'target_grade': forms.Select(attrs={'class': 'form-select', 'id': 'id_target_grade'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class LectureScheduleForm(forms.ModelForm):
    """講義スケジュール登録・編集フォーム"""

    weekday = forms.ChoiceField(
        choices=LectureSchedule.Weekday.choices,
        label="曜日",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    subject = forms.CharField(
        label="科目名",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "例：プログラミング実習２",
            "autofocus": True,
        }),
    )

    canceled_date = forms.DateField(
        label="休講日",
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date",  # これでブラウザ標準のカレンダーが出ます
            "id": "id_canceled_date",
        }),
        help_text="※特定の日だけを休講にする場合に選択してください。毎週の場合は空欄のままでOK。"
    )

    start_period = forms.ModelChoiceField(
        queryset=SchoolPeriod.objects.all(),
        label="開始時限",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    end_period = forms.ModelChoiceField(
        queryset=SchoolPeriod.objects.all(),
        label="終了時限",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    User = get_user_model()
    teacher = forms.CharField(
        label="担当教員",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "未選択の場合は空欄",
            "autofocus": True,
        }),
    )

    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        required=False,
        label="教室",
        widget=forms.Select(attrs={
            "class": "form-select",
            "data-placeholder": "未定の場合は空欄",
        }),
    )

    status = forms.ChoiceField(
        choices=LectureSchedule.Status.choices,
        label="講義状態",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    note = forms.CharField(
        required=False,
        label="備考",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "補足事項や休講理由があれば記入してください",
        }),
    )

    class Meta:
        model = LectureSchedule
        fields = [
            "weekday",
            "subject",
            "canceled_date",
            "start_period",
            "end_period",
            "teacher",
            "room",
            "status",
            "note",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Select 系の空ラベル統一
        for field in ["start_period", "end_period", "room"]:
            self.fields[field].empty_label = "---------"

    def clean(self):
        """
        カスタムバリデーション:
        開始時限が終了時限よりも後になっていないかを確認する。
        """
        cleaned_data = super().clean()
        start_period = cleaned_data.get("start_period")
        end_period = cleaned_data.get("end_period")

        if start_period and end_period:
            # SchoolPeriod オブジェクトの比較:
            # ここでは SchoolPeriod モデルに時限の順序を示すフィールド (例: `period_number`, `order`, `pk` など)
            # があり、それを比較に利用できることを前提とします。
            # 例として、PK (Primary Key) が時限の順序を表していると仮定します。
            if start_period.pk > end_period.pk:
                # フォーム全体ではなく、関連するフィールドにエラーを割り当てる
                msg = "終了時限は開始時限以降である必要があります。"
                self.add_error('end_period', msg)

                # Globalなエラーとして表示したい場合は以下を使用:
                # raise ValidationError("終了時限は開始時限以降である必要があります。", code='invalid_period_range')

        return cleaned_data


class EventForm(forms.ModelForm):
    """イベント登録・編集フォーム"""

    title = forms.CharField(
        label="イベント名",
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "例：紅華祭 / 試験期間 / 休校日",
            "autofocus": True,
        }),
    )

    start_date = forms.DateField(
        label="開始日",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
        }),
    )

    end_date = forms.DateField(
        label="終了日",
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
        }),
    )

    description = forms.CharField(
        required=False,
        label="説明",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "必要に応じて詳細を入力してください",
        }),
    )

    target_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="対象学科（未選択なら全学科）",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    target_grade = forms.ChoiceField(
        choices=[("", "全学年")] + list(Profile.GRADE_CHOICES),
        required=False,
        label="対象学年（未選択なら全学年）",
        widget=forms.Select(attrs={
            "class": "form-select",
        }),
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "start_date",
            "end_date",
            "target_department",
            "target_grade",
            "description",
        ]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end and start > end:
            self.add_error(
                "end_date",
                "終了日は開始日以降でなければなりません。"
            )

        return cleaned_data
