"""
Django URL Configuration
"""
<<<<<<< HEAD
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
=======
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.views.generic import TemplateView
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def home_redirect(request):
    return redirect('/api/v1/health/')

urlpatterns = [
<<<<<<< HEAD
    path('', home_redirect, name='home'),
=======
    # API endpoints
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
    path('api/v1/', include('api.urls')),
    
    # Swagger Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
<<<<<<< HEAD
=======
    
    # Health check alias
    path('api/health/', home_redirect),
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
]

# Serve static and media (development and production)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
<<<<<<< HEAD
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Frontend Integration (Catch-all)
# This must be the last pattern
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
