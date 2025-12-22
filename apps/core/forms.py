from django import forms
from .models import ReceivedEmail

class AnnouncementForm(forms.ModelForm):
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
    
    