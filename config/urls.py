from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # ホームページ
    path('', include('apps.core.urls')),

    # ユーザ登録ページ
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # 管理者ページ
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
