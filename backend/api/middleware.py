"""
API Key Authentication and Rate Limiting for Yemen LPR System
"""

import logging
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone

from .models import APIKey
from .rate_limit import is_rate_limited, get_remaining

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """Add X-Frame-Options, CSP when not DEBUG."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.DEBUG and hasattr(response, "headers"):
            response.setdefault("X-Frame-Options", "DENY")
            response.setdefault("X-Content-Type-Options", "nosniff")
            csp = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self'; font-src 'self';"
            response.setdefault("Content-Security-Policy", csp)
        return response


def _get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "127.0.0.1")


class RateLimitMiddleware:
    """60 requests per minute per IP (configurable via API_RATE_LIMIT_PER_MINUTE)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = getattr(settings, "API_RATE_LIMIT_PER_MINUTE", 60)

    def __call__(self, request):
        path = request.path
        if not path.startswith("/api/"):
            return self.get_response(request)
        if path.startswith("/api/v1/health") or path.startswith("/api/v1/docs") or path.startswith("/api/v1/api-keys/"):
            return self.get_response(request)
        ip = _get_client_ip(request)
        if is_rate_limited(ip, limit=self.limit):
            return JsonResponse(
                {
                    "success": False,
                    "error": "Rate limit exceeded",
                    "message": f"Max {self.limit} requests per minute.",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                },
                status=429,
            )
        response = self.get_response(request)
        rem = get_remaining(ip, limit=self.limit)
        if rem is not None and hasattr(response, "headers"):
            response["X-RateLimit-Remaining"] = str(rem)
        return response


class APIKeyMiddleware:
    """
    Middleware to validate API keys for protected endpoints.

    - When DEBUG=False: require a valid key.
    - When DEBUG=True: log presence only.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            "/api/v1/predict/image/",
            "/api/v1/predict/video/",
        ]

        is_protected_path = any(request.path.startswith(path) for path in protected_paths)
        if is_protected_path:
            api_key = request.META.get("HTTP_X_API_KEY")

            if not settings.DEBUG:
                if not api_key:
                    return JsonResponse(
                        {"error": "API key required", "message": "X-API-Key header is missing"},
                        status=401,
                    )

                try:
                    key_obj = APIKey.objects.get(key=api_key, is_active=True)
                except APIKey.DoesNotExist:
                    return JsonResponse(
                        {"error": "Invalid API key", "message": "The provided API key is invalid or inactive"},
                        status=401,
                    )

                key_obj.usage_count += 1
                key_obj.last_used = timezone.now()
                key_obj.save(update_fields=["usage_count", "last_used"])
            else:
                if api_key:
                    logger.info("API Key provided in development: %s...", api_key[:10])
                else:
                    logger.info("No API key provided in development mode")

        return self.get_response(request)

