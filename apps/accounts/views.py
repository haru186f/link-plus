from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Faculty, Department, Course


def signup_view(request):
    """
    新規ユーザー登録ビュー
    登録後、自動的にログインしてホーム画面へリダイレクト
    """
    faculties = Faculty.objects.all()  # 学部リストを取得

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='apps.accounts.backends.UsernameOrEmailBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form, 'faculties': faculties})


def login_view(request):
    """
    ログインビュー（ユーザー名またはメールアドレスで認証）
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # "next" パラメータがある場合はそのURLへ、それ以外は home へ
            return redirect(request.GET.get('next', 'home'))
    else:
        form = CustomAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    ログアウト処理
    """
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    """
    ログイン後のホーム画面
    """
    return render(request, 'accounts/home.html')



def get_departments(request):
    """
    学部選択時に学科を返す
    """
    faculty_id = request.GET.get("faculty_id")
    departments = Department.objects.filter(faculty_id=faculty_id).values("id", "name")
    return JsonResponse(list(departments), safe=False)


def get_courses(request):
    """
    学科選択時にコースを返す
    """
    department_id = request.GET.get("department_id")
    courses = Course.objects.filter(department_id=department_id).values("id", "name")
    return JsonResponse(list(courses), safe=False)
