from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.bus.models import BusStop
from apps.lecture.models import College, Department, Course


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
    """カスタムユーザーモデル"""

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    username = None # usernameフィールドを無効化

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    """ユーザプロフィールモデル"""

    GRADE_CHOICES = [(i, f"{i}年") for i in range(1, 5)]
    CLASS_CHOICES = [(i, f"{i}組") for i in range(1, 5)]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile")
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    bus_stop = models.ForeignKey(BusStop, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.IntegerField(_("grade"), null=True, blank=True, choices=GRADE_CHOICES)
    class_number = models.IntegerField(_("class"), null=True, blank=True, choices=CLASS_CHOICES)

    def __str__(self):
        return f"Profile of {self.user.email}"
