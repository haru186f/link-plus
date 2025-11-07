# apps/accounts/admin.py
from django.contrib import admin
from .models import College, Department, Course, CustomUser

admin.site.register(College)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CustomUser)
