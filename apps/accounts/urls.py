from django.urls import path
from .views import SignupView, CustomLoginView, ProfileView


app_name='accounts'
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
