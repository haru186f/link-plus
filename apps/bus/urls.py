from django.urls import path
from . import views



app_name = "bus"

urlpatterns = [
    path("", views.next_bus_times, name="next_bus_times"),
]
