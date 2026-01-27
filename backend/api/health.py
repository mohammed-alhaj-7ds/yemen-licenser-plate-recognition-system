from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

@csrf_exempt
def health_check(request):
    """
    Lightweight health check endpoint.
    No DB, No AI, No Heavy Imports.
    Returns 200 OK.
    """
    return JsonResponse({"status": "ok"})
