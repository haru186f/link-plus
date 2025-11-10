from django.urls import path
from . import views

# URLconf は urlpatterns というリスト変数でなければなりません
urlpatterns = [
    # Webhook 受信用URL
    # 外部サービス (SendGrid, Mailgunなど) がメールを送信するエンドポイント
    # 例: /api/email/webhook/ への POSTリクエストを処理
    path('webhook/', views.receive_email_webhook, name='email_webhook'),
    
    # 必要に応じて、メール一覧表示などのビューをここに追加できます
    # path('', views.EmailListView.as_view(), name='email_list'), 
]