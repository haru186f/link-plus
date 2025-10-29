from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('signup/done/', SignupDoneView.as_view(), name='signup_done'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('ajax/get-departments/', GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
]
