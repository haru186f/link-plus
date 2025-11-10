from django.urls import path
from .views import *

app_name = 'lecture'
urlpatterns = [
    # Ajaxエンドポイント
    path('ajax/get-departments/', GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
    path('ajax/get-grades/', GetGradesView.as_view(), name="get_grades"),
]
