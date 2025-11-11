from django.urls import path
from .views import HomeView
from . import views

app_name = 'news'

# URLconf は urlpatterns というリスト変数でなければなりません
urlpatterns = [
    # Webhook 受信用URL
    path('webhook/', views.receive_email_webhook, name='email_webhook'),
    
    # 必要に応じて、メール一覧表示などのビューをここに追加できます
    # path('', views.EmailListView.as_view(), name='email_list'), 
    path('', HomeView.as_view(), name='home'),
]
