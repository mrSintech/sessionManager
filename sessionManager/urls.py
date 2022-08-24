from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

# Tools
from core import tools

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls', namespace="core_api")),
    path('auth/', include('authentication.urls', namespace="auth_api")),
    
    # Media Access
    re_path(r'^media/public/(?P<url>.*)', tools.public_media_access, {'document_root': settings.MEDIA_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
