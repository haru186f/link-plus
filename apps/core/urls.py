from django.urls import path
from .views import HomeView
from .views import GetDepartmentsView, GetCoursesView, GetGradesView, NewsListView
from .views import receive_email_webhook, api_email_body, lecture_events, GetNextBusInfo, DebugBusSchedule
from . import views

app_name = 'core'
urlpatterns = [
    # ホームページ
    path('', HomeView.as_view(), name='home'),

    # お知らせ一覧
    path('news/', NewsListView.as_view(), name='news_list'),

    # エンドポイント
    path('ajax/get-departments/', GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
    path('ajax/get-grades/', GetGradesView.as_view(), name="get_grades"),
    path('webhook/', receive_email_webhook, name='email_webhook'),
    path('api/body/<int:pk>/', api_email_body, name='api_email_body'),
    path('api/lecture-events/', lecture_events, name='lecture_events'),
<<<<<<< HEAD
    path('api/bus-schedules/', views.get_data_for_modal, name='get_modal_data'),
    path("api/bus/next/", GetNextBusInfo.as_view(), name="api_next_bus")
||||||| parent of 687a929 (feat: ニュース一覧画面にホームに戻るボタンを追加)
    path("api/bus/next/", GetNextBusInfo.as_view(), name="api_next_bus")
=======
    path("api/bus/next/", GetNextBusInfo.as_view(), name="api_next_bus"),
    path("api/debug-bus/", DebugBusSchedule.as_view(), name="debug_bus")
>>>>>>> 687a929 (feat: ニュース一覧画面にホームに戻るボタンを追加)
]
