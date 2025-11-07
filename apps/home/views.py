from django.shortcuts import render
from apps.bus.models import BusSchedule

def index(request):
    next_buses = BusSchedule.objects.order_by('departure_time')[:5]
    context = {
        'next_buses': next_buses,
    }
    return render(request, 'home/index.html', context)
