"""
Unified response schemas for API endpoints
"""
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from typing import Dict, Optional, Any


class APIResponse:
    """Unified API response formatter"""
    
    @staticmethod
    def success(
        data: Dict[str, Any],
        message: Optional[str] = None,
        status_code: int = status.HTTP_200_OK
    ) -> Response:
        """Format successful response"""
        response_data = {
            "success": True,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        if message:
            response_data["message"] = message
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(
        error: str,
        message: Optional[str] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict] = None
    ) -> Response:
        """Format error response"""
        response_data = {
            "success": False,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        if message:
            response_data["message"] = message
        if details:
            response_data["details"] = details
        return Response(response_data, status=status_code)
    
    @staticmethod
    def health_check(model_loaded: bool = True) -> Response:
        """Format health check response"""
        return Response({
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "model_loaded": model_loaded
        })
