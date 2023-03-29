from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('', include('checks.urls')),
]

urlpatterns = [
    path('api/v1/', include(api_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
