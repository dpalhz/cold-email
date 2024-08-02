
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('email/', include('sendingemail.urls')),
    path('email-data/', include('email_data.urls')),
    path('generator/', include('generator_message.urls')),
    path('', include('dashboard.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls'))
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)