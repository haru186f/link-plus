from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
]


# urlpatterns = [
#     path('', .as_view(), name=''),
# ]
