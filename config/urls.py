from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD
    path('', include('apps.home.urls')),        # その他
    path('lecture/', include('apps.lecture.urls')),     # 講義
    path('news/', include('apps.news.urls')),        # お知らせ
    path('bus/', include('apps.bus.urls')),         # バス時刻
||||||| 80b9e94
    path('', include('apps.core.urls')),
=======
    path('', include('apps.core.urls')),        # その他
    path('', include('apps.lecture.urls')),     # 講義
    path('', include('apps.news.urls')),        # お知らせ
    path('', include('apps.bus.urls')),         # バス時刻
>>>>>>> origin/main
    path('accounts/', include('apps.accounts.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
