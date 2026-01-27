from datetime import datetime
from typing import Dict, Optional, Tuple, Any

class ResponseFormatter:
    """Unified response formatter for API endpoints"""
    
    @staticmethod
    def success(data: Dict, message: Optional[str] = None) -> Dict:
        """Format successful response"""
        response = {
            "success": True,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
        if message:
            response["message"] = message
        return response
    
    @staticmethod
    def error(
        error: str, 
        message: Optional[str] = None, 
        status_code: int = 400
    ) -> Tuple[Dict, int]:
        """Format error response"""
        response = {
            "success": False,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        }
        if message:
            response["message"] = message
        return response, status_code
    
    @staticmethod
    def health_check(model_loaded: bool = True) -> Dict:
        """Format health check response"""
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "model_loaded": model_loaded
        }
