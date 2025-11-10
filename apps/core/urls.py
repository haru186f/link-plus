from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name='home'),
]

# 例：
# urlpatterns = [
#     path('', .as_view(), name=''),
# ]
