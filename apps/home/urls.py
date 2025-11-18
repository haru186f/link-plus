from django.urls import path
from apps.news.views import HomeView # 🚨 HomeViewはnewsアプリにあると仮定

urlpatterns = [
    # サイトのルートパス('/')をHomeViewが担当する
    path('', HomeView.as_view(), name='home'),
]
