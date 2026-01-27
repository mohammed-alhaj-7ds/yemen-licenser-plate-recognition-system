"""
API Middleware
- Rate Limiting
- API Key Authentication
- Security Headers
- Exception Handling
"""
import time
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from .models import APIKey

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add basic security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            return self.get_response(request)
            
        # Simple IP-based rate limiting
        ip = self.get_client_ip(request)
        cache_key = f"rate_limit_{ip}"
        
        # Allow health checks bypass
        if request.path.endswith('/health/'):
            return self.get_response(request)

        # Get request count
        request_count = cache.get(cache_key, 0)
        
        if request_count >= settings.API_RATE_LIMIT_PER_MINUTE:
            return JsonResponse({
                "error": "too_many_requests",
                "message": "Rate limit exceeded. Please try again later."
            }, status=429)
            
        # Increment and set expiry (60 seconds)
        if request_count == 0:
            cache.set(cache_key, 1, 60)
        else:
            cache.incr(cache_key)
            
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Whitelisted paths that don't require API key
        self.whitelist = [
            '/api/v1/health/',
            '/api/health/',
            '/api/docs/',
            '/api/schema/',
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico',
        ]

    def __call__(self, request):
        # 1. Bypass whitelist
        if any(request.path.startswith(path) for path in self.whitelist):
            return self.get_response(request)
            
        # 2. Bypass Frontend (if serving frontend from same domain)
        # Usually frontend assets or root / don't need auth, but API endpoints do.
        # If request is NOT for /api/, bypass
        if not request.path.startswith('/api/'):
            return self.get_response(request)

        # 3. Check API Key
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            # Allow creating keys without being authenticated? Typically no, but creating key might be protected differently
            # For now, if path is /api-keys/create/, maybe allow?
            if request.path == '/api/v1/api-keys/create/':
                 return self.get_response(request)
                 
            return JsonResponse({
                "error": "unauthorized",
                "message": "Missing API Key. Provide 'X-API-Key' header."
            }, status=401)

        # 4. Validate Key
        try:
            if not APIKey.objects.filter(key=api_key, is_active=True).exists():
                return JsonResponse({
                    "error": "forbidden",
                    "message": "Invalid or inactive API Key."
                }, status=403)
        except Exception:
            # DB error or during migration (if table doesn't exist yet)
            pass

        return self.get_response(request)

class SafeExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # Log exception here
        return JsonResponse({
            "error": "internal_error",
            "message": "An unexpected error occurred."
        }, status=500)
