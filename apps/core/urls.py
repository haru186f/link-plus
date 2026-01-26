from django.urls import path
from .views import HomeView
from .views import GetDepartmentsView, GetCoursesView, GetGradesView, NewsListView, NewsCreateView
from .views import receive_email_webhook, api_email_body, lecture_events, get_data_for_modal
from .views import GetNextBusInfo, EventCreateView, all_day_events, DebugBusSchedule
from .views import LectureScheduleListView, LectureScheduleCreateView, LectureScheduleUpdateView, LectureScheduleDeleteView

app_name = 'core'
urlpatterns = [
     # ホームページ
     path('', HomeView.as_view(), name='home'),

     # お知らせ
     path('news/', NewsListView.as_view(), name='news_list'),
     path('news/create/', NewsCreateView.as_view(), name='news_create'),

     # 講義
     path('lectures/', LectureScheduleListView.as_view(), name='lecture_list'),
     path('lectures/create/', LectureScheduleCreateView.as_view(), name="lecture_create"),
     path('lectures/<int:pk>/update/', LectureScheduleUpdateView.as_view(), name="lecture_update"),
     path('lectures/<int:pk>/delete/', LectureScheduleDeleteView.as_view(), name="lecture_delete"),

     # イベント
     path("events/create/", EventCreateView.as_view(), name="event_create"),

     # エンドポイント
     path('ajax/get-departments/', GetDepartmentsView.as_view(), name="get_departments"),
     path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
     path('ajax/get-grades/', GetGradesView.as_view(), name="get_grades"),
     path('webhook/', receive_email_webhook, name='email_webhook'),
     path('api/body/<int:pk>/', api_email_body, name='api_email_body'),
     path('api/lecture-events/', lecture_events, name='lecture_events'),
     path('api/bus-schedules/', get_data_for_modal, name='get_modal_data'),
     path("api/bus/next/", GetNextBusInfo.as_view(), name="api_next_bus"),
     path("api/debug-bus/", DebugBusSchedule.as_view(), name="debug_bus"),
     path('api/next/', GetNextBusInfo.as_view(), name='get_next_bus_info'),
     path("api/all-day-events/", all_day_events, name="all_day_events",),
]
