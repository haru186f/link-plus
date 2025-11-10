from django.urls import path

from . import views

app_name='accounts'
urlpatterns = [
    # ユーザログインページ
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]
