from django.contrib.auth import login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignupForm, CustomAuthenticationForm, ProfileForm
from apps.core.models import College
from .models import Profile


User = get_user_model()
class SignupView(CreateView):
    """ユーザ登録ビュー"""
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy("accounts:profile")  # プロフィール設定画面に遷移

    def form_valid(self, form):
        """ユーザ登録後に自動ログインを行う"""
        response = super().form_valid(form)         # まずユーザを保存し、self.object に代入
        user = self.object                          # Django が保存した User インスタンス
        login(self.request, user)                   # 登録後に自動ログイン
        Profile.objects.get_or_create(user=user)    # プロフィールを作成（重複防止）
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """ユーザプロフィール更新ビュー"""
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('core:home')         # ホーム画面へ
    login_url = reverse_lazy('accounts:login')      # 未ログインのときログインページへ飛ばす

    def get_object(self):
        """現在のユーザのプロフィールを取得（なければ作成）"""
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_context_data(self, **kwargs):
        """カレッジリストをテンプレートに渡す"""
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        return context


class CustomLoginView(LoginView):
    """カスタムログインビュー"""
    template_name = 'registration/login.html'
    success_url = reverse_lazy('core:home')
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('core:home')
