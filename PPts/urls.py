from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .admin_ratelimit import login_wrapper

admin.autodiscover()
admin.site.login = login_wrapper(admin.site.login)

urlpatterns = [
    path('hostmaster/', admin.site.urls),
    path('', include('Site.urls', namespace='Site')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
