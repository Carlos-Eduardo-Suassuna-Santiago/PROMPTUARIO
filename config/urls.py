"""
Configuração de URLs do projeto Promptuario.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical-records/', include('medical_records.urls')),
    path('reports/', include('reports.urls')),
    
    # Redirect root to login
    path('', RedirectView.as_view(pattern_name='accounts:login', permanent=False)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Promptuario - Administração"
admin.site.site_title = "Promptuario Admin"
admin.site.index_title = "Bem-vindo ao Promptuario"

from .views import healthcheck

urlpatterns.append(path('healthcheck/', healthcheck, name='healthcheck'))
