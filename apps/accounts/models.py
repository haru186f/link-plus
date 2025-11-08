from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# カレッジ（例：ITカレッジ）
class College(models.Model):
    name = models.CharField(max_length=100)
    max_grade = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.name


# 学科（例：情報処理科）
class Department(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name


# コース（例：システム開発コース）
class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name


# バス停（例：八王子みなみ野）
class Bus(models.Model):
    BUS_CHOICES = [('hachiouji', '八王子'), ('minamino', '八王子みなみ野')]
    name = models.CharField(max_length=20, choices=BUS_CHOICES, default='hachiouji')
    def __str__(self):
        return self.name


class CustomUserManager(UserManager):
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


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_teacher = models.BooleanField(_("teacher status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    GRADE_CHOICES = [(i, f"{i}年") for i in range(1, 5)]
    grade = models.IntegerField(_("grade"), choices=GRADE_CHOICES, blank=True, null=True)

    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


