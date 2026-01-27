"""
Safe Exception Handling Middleware
Catches 500 errors and returns safe JSON responses.
"""
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class SafeExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"Internal Server Error: {str(exception)}", exc_info=True)
        return JsonResponse({
            "error": "internal_error",
            "message": "An internal error occurred. Our team has been notified."
        }, status=500)
