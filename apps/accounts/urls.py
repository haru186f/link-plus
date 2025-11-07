from django.urls import path

from . import views

app_name='accounts'
urlpatterns = [
    # ユーザログインページ
    path('signup/', views.SignupView.as_view(), name='signup'),

    # Ajaxエンドポイント
    path('ajax/get-departments/', views.GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', views.GetCoursesView.as_view(), name="get_courses"),
    path('ajax/get-grades/', views.GetGradesView.as_view(), name="get_grades"),
]
