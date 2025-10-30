from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Faculty, Department, Course


class SignupView(CreateView):
    """
    新規登録ビュー
    登録後、自動的にログインしてホーム画面へリダイレクト
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        """学部リストをテンプレートへ渡す"""
        context = super().get_context_data(**kwargs)
        context['faculties'] = Faculty.objects.all()
        return context

    def form_valid(self, form):
        """フォームが有効な場合、ユーザーを保存し自動ログイン"""
        user = form.save()
        login(self.request, user, backend='apps.accounts.backends.UsernameOrEmailBackend')
        return redirect(self.get_success_url())


class SignupDoneView(TemplateView):
    """
    新規登録完了ビュー
    """
    template_name = 'registration/signup_done.html'


class CustomLoginView(LoginView):
    """
    ログインビュー
    """
    template_name = 'registration/login.html'  # ← Django 標準に合わせた
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        """ログイン後リダイレクト先を決定"""
        return self.request.GET.get('next', reverse_lazy('home'))


class CustomLogoutView(LogoutView):
    """
    ログアウト処理
    """
    next_page = reverse_lazy('login')


class HomeView(LoginRequiredMixin, TemplateView):
    """
    ログイン後のホーム画面
    """
    template_name = 'accounts/home.html'


class GetDepartmentsView(View):
    """
    学部選択時に学科を返す（Ajax）
    """
    def get(self, request, *args, **kwargs):
        faculty_id = request.GET.get("faculty_id")
        departments = Department.objects.filter(faculty_id=faculty_id).values("id", "name")
        return JsonResponse(list(departments), safe=False)


class GetCoursesView(View):
    """
    学科選択時にコースを返す（Ajax）
    """
    def get(self, request, *args, **kwargs):
        department_id = request.GET.get("department_id")
        courses = Course.objects.filter(department_id=department_id).values("id", "name")
        return JsonResponse(list(courses), safe=False)
