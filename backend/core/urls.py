"""
Django URL Configuration
"""
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.health import health_check

urlpatterns = [
    # API endpoints
    path('api/v1/', include('api.urls')),
    
    # Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Health check (Direct 200 OK, no redirect)
    path('api/health/', health_check, name='health_check_main'),
]

# Serve static and media (development and production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Frontend Integration (Catch-all)
# This must be the last pattern
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]