from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    """Define a model for User model with no username field."""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_teacher", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_teacher", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_teacher") is not True:
            raise ValueError("Superuser must have is_teacher=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""

    class Meta:
        db_table = "custom_user"
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー"

    username = None                     # usernameフィールドを無効化
    first_name = None                   # first_nameフィールドを無効化
    last_name = None                    # last_nameフィールドを無効化

    email = models.EmailField(          # メールアドレス（ログインに必須）
        _("email address"),
        unique=True
    )

    is_staff = models.BooleanField(     # 管理サイトにログイン可能か（default=False）
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )

    is_active = models.BooleanField(    # 有効なユーザーアカウントか（default=True）
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_teacher = models.BooleanField(   # 教師専用機能を利用可能か（default=False）
        _("teacher status"),
        default=False,
        help_text=_(
            "Designates whether the user can access teacher-only features."
        ),
    )

    date_joined = models.DateTimeField( # 作成日
        _("date joined"),
        default=timezone.now
    )

    objects = CustomUserManager()       # カスタムユーザマネージャーを指定

    USERNAME_FIELD = "email"            # usernameフィールドをemailで上書き
    REQUIRED_FIELDS = []                # 空にすると、メールアドレス＆パスワードのみでsuperuserを作成できる

    def __str__(self):
        return self.email


class Profile(models.Model):
    """ユーザプロフィールモデル"""

    GRADE_CHOICES = [(i, f"{i}年") for i in range(1, 5)]
    CLASS_CHOICES = [(i, f"{i}組") for i in range(1, 5)]

    grade = models.PositiveIntegerField(            # 学年
        _("grade"),
        null=True,
        blank=True,
        choices=GRADE_CHOICES
    )

    class_number = models.PositiveIntegerField(     # クラス
        _("class"),
        null=True,
        blank=True,
        choices=CLASS_CHOICES
    )

    # 外部キー
    user = models.OneToOneField(            # ユーザー
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name="profile",
    )

    college = models.ForeignKey(            # カレッジ
        'core.College',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )

    department = models.ForeignKey(         # 学科
        'core.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )

    course = models.ForeignKey(             # コース
        'core.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )

    bus_stop = models.ForeignKey(           # バス
        'core.BusStop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles",
    )

    def __str__(self):
        return f"Profile of {self.user.email if self.user else 'Unknown'}"

