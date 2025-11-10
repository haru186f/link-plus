from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from apps.lecture.models import College

User = get_user_model()
class SignupView(CreateView):
    """
    ユーザ登録ビュー
    登録後に自動ログインし、ホーム画面へリダイレクトする
    """
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        """カレッジリストをテンプレートに渡す"""
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        return context

    def form_valid(self, form):
        """ユーザ登録後に自動ログインを行う"""
        valid = super().form_valid(form)
        # 登録直後のユーザをログイン状態にする
        login(self.request, self.object)
        return valid


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login')
    authentication_form = CustomAuthenticationForm
