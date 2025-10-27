from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def signup_view(request):
    """
    新規ユーザー登録ビュー
    登録後、自動的にログインしてホーム画面へリダイレクト
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # バックエンドを指定（ユーザー名またはメールアドレスログイン対応）
            login(request, user, backend='apps.accounts.backends.UsernameOrEmailBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


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
