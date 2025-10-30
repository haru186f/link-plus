from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name="core/home.html"
    login_url = 'accounts/login/'
    redirect_field_name = 'next'
