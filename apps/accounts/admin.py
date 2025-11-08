# apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import College, Department, Course, CustomUser

class CustomUserAdmin(UserAdmin):
    # 「まずユーザー名とパスワードを登録してください。」という文言を非表示にする
    add_form_template = None
    # 表示項目から username を削除して email に変更
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'college', 'department', 'course', 'grade', 'bus')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_teacher', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'college', 'department', 'grade', 'bus', 'is_teacher', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)




admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)
