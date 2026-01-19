from django.urls import path
from .views import HomeView
from . import views
from .views import GetDepartmentsView, GetCoursesView, GetGradesView, NewsListView
from .views import receive_email_webhook, api_email_body, lecture_events, get_data_for_modal
from .views import GetNextBusInfo, DebugBusSchedule
from .views import LectureScheduleListView, LectureScheduleCreateView, LectureScheduleUpdateView, LectureScheduleDeleteView
from .views import internal_events_api, external_events_api
from .views import InternalEventCreateView, ExternalEventCreateView


app_name = 'core'
urlpatterns = [
    # ホームページ
    path('', HomeView.as_view(), name='home'),

    # お知らせ
    path('news/', NewsListView.as_view(), name='news_list'),
    path('announcement/new/', views.announcement_create,
         name='announcement_create'),
    # path('news/create/', NewsCreateView.as_view(), name="news_create"),

    # 時間割
    path('timetable/', LectureScheduleListView.as_view(),
         name='lecture_schedule_list'),
    path('timetable/create/', LectureScheduleCreateView.as_view(),
         name="lecture_schedule_create"),
    path('timetable/<int:pk>/update/', LectureScheduleUpdateView.as_view(),
         name="lecture_schedule_update"),
    path('timetable/<int:pk>/delete/', LectureScheduleDeleteView.as_view(),
         name="lecture_schedule_delete"),

    # イベント
    path(
        "events/internal/create/",
        InternalEventCreateView.as_view(),
        name="internal_event_create",
    ),
    path(
        "events/external/create/",
        ExternalEventCreateView.as_view(),
        name="external_event_create",
    ),

    # エンドポイント
    path('ajax/get-departments/',
         GetDepartmentsView.as_view(), name="get_departments"),
    path('ajax/get-courses/', GetCoursesView.as_view(), name="get_courses"),
    path('ajax/get-grades/', GetGradesView.as_view(), name="get_grades"),
    path('webhook/', receive_email_webhook, name='email_webhook'),
    path('api/body/<int:pk>/', api_email_body, name='api_email_body'),
    path('api/lecture-events/', lecture_events, name='lecture_events'),
    path('api/bus-schedules/', get_data_for_modal, name='get_modal_data'),
    path("api/bus/next/", GetNextBusInfo.as_view(), name="api_next_bus"),
    path("api/debug-bus/", DebugBusSchedule.as_view(), name="debug_bus"),
    path('api/next/', GetNextBusInfo.as_view(), name='get_next_bus_info'),
    path("api/events/internal/", internal_events_api, name="internal_events",),
    path("api/events/external/", external_events_api, name="external_events",)
]
