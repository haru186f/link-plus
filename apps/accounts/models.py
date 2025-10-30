from django.contrib.auth.models import AbstractUser
from django.db import models


# 学部（例：ITカレッジ）
class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 学科（例：情報処理科）
class Department(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')

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

      
# カスタムユーザー
class CustomUser(AbstractUser):
    GRADE_CHOICES = [(i, f"{i}年") for i in range(1, 5)]
    ROLE_CHOICES = [(1, '学生'), (2, '教員'), (3, '管理者')]

    email = models.EmailField(unique=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, blank=True, null=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    bus = models.ForeignKey('Bus', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


