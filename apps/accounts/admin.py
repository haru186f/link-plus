# apps/accounts/admin.py
from django.contrib import admin
from .models import Faculty, Department, Course, CustomUser

admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CustomUser)
