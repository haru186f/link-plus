from django.shortcuts import render
from apps.bus.models import BusSchedule
from apps.lecture.models import Schedule
from django.views.generic import TemplateView

class HomeIndexView(TemplateView):

    template_name = 'core/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schedules'] = Schedule.objects.filter()
        return context
