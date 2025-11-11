from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import SignupForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from apps.lecture.models import College
from .models import Profile


User = get_user_model()


class SignupView(CreateView):
    """ユーザ登録ビュー"""
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy("signup_done")  # 登録完了ページ

    def form_valid(self, form):
        """ユーザ登録後に自動ログインを行う"""
        user = form.save()
        login(self.request, user)  # 登録後に自動ログイン
        Profile.objects.create(user=user)  # 空のプロフィール作成
        return super().form_valid(form)


class ProfileView(UpdateView):
    """ユーザプロフィール更新ビュー"""
    model = Profile
    form_class = PfofileForm
    template_name = 'registrations/profile.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """カレッジリストをテンプレートに渡す"""
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        return context

    def get_object(self, queryset=None):
        """現在のユーザのプロフィールを取得"""
        return Profile.objects.get(user=self.request.user)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login')
    authentication_form = CustomAuthenticationForm
