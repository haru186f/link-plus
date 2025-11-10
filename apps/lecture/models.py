from django.db import models

# Create your models here.
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
