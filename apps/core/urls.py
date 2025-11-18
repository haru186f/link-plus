from django.urls import path
from .views import HomeView, GetDepartmentsView, GetCoursesView, GetGradesView, receive_email_webhook

app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # エンドポイント
    path('ajax/get-departments/', GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
    path('ajax/get-grades/', GetGradesView.as_view(), name="get_grades"),
    path('webhook/', receive_email_webhook, name='email_webhook'),
]
