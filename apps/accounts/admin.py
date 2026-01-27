from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Profile


class ProfileInline(admin.StackedInline):
    """ユーザープロフィールをユーザー管理画面に表示"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'プロフィール'
    fk_name = 'user'
    classes = ("collapse",)
    extra = 0


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form_template = None
    inlines = (ProfileInline,)

    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_teacher',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'is_teacher', 'is_active', 'date_joined')

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
