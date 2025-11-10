from django.urls import path

from .views import *

app_name='accounts'
urlpatterns = [
    # ユーザログインページ
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
