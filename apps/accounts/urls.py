from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ajax/get-departments/', views.get_departments, name="get_departments"),
    path('ajax/get-courses/', views.get_courses, name="get_courses"),
    path('', views.home_view, name='home'),
]
