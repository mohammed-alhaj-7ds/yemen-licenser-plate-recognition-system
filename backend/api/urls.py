"""
Django API URLs
"""
from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('predict/image/', views.predict_image, name='predict_image'),
    path('predict/video/', views.predict_video, name='predict_video'),
    path('docs/', views.api_docs, name='api_docs'),
    path('api-keys/create/', views.create_api_key, name='create_api_key'),
]
