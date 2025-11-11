from apps.home.views import MasterHomeView 
from django.urls import path, include
# from apps.news.views import receive_email_webhook # Webhookはnewsアプリにそのまま残す

urlpatterns = [
    # ルートパスは MasterHomeView に一本化！
    path('', MasterHomeView.as_view(), name='home'),
    
    # ... (Webhookや他のURL定義が続く)
]
