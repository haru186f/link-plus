from django.contrib import admin
from .models import BusStop, BusSchedule

# Register your models here.

admin.site.register(BusStop)
admin.site.register(BusSchedule)
