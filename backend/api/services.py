"""
Business logic services for License Plate Recognition API
Separated from views for better organization and testability
"""
import os
import uuid
import cv2
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

from django.conf import settings

# Add parent directory to path for AI imports
sys.path.insert(0, str(settings.BASE_DIR.parent))

from ai.pipeline import process_image, process_video


class PlateRecognitionService:
    """Service for handling plate recognition operations"""
    
    def __init__(self):
        self.upload_dir = settings.MEDIA_ROOT / 'uploads'
        self.results_dir = settings.MEDIA_ROOT / 'results'
        self.videos_dir = settings.MEDIA_ROOT / 'results'
        
        # Create directories if they don't exist
        for dir_path in [self.upload_dir, self.results_dir, self.videos_dir]:
            os.makedirs(dir_path, exist_ok=True)
    
    def save_uploaded_file(self, uploaded_file, keep_original: bool = True) -> Tuple[Path, str]:
        """
        Save uploaded file. Originals kept in uploads/; used for processing.
        Returns (file_path, filename).
        """
        ext = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        base = "original" if keep_original else "upload"
        filename = f"{base}_{uuid.uuid4().hex}{ext}"
        path = self.upload_dir / filename
        with open(path, "wb") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)
        return path, filename
    
    def draw_overlay(self, image_path: Path, detections: List[Dict]) -> Optional[str]:
        """
        Draw bounding boxes and labels on image
        
        Returns:
            Output filename if successful, None otherwise
        """
        img = cv2.imread(str(image_path))
        if img is None:
            return None
        
        for det in detections:
            bbox = det.get("bbox")
            text = det.get("plate_number", "")
            conf = det.get("detection_confidence", 0)
            
            if bbox and len(bbox) == 4:
                x1, y1, x2, y2 = map(int, bbox)
                color = (0, 200, 0) if conf > 0.7 else (0, 165, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
                
                label = f"{text} ({conf:.0%})" if text else "—"
                (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(img, (x1, y1 - th - 12), (x1 + tw + 12, y1), color, -1)
                cv2.putText(img, label, (x1 + 6, y1 - 6),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        out_name = f"result_{uuid.uuid4().hex[:12]}.png"
        out_path = self.results_dir / out_name
        cv2.imwrite(str(out_path), img)
        return out_name
    
    def process_image_file(
        self, 
        uploaded_file, 
        overlay: bool = True,
        save_crops: bool = True
    ) -> Dict:
        """
        Process uploaded image file for plate detection
        
        Returns:
            Dictionary with results and metadata
        """
        path, _ = self.save_uploaded_file(uploaded_file, keep_original=True)
        try:
            results = process_image(
                str(path),
                save_crops=save_crops,
                crops_dir=self.upload_dir.parent / "crops",
                logs_dir=Path(__file__).resolve().parents[2] / "output" / "logs",
                debug_gov=True,
            )
            
            # New structure handling
            response_data = {
                "success": True,
                "results": results.get("plates", []),
                "vehicles": results.get("vehicles", []),
                "confidence_summary": results.get("confidence", {}),
                "plates_found": len(results.get("plates", [])),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
            
            if overlay and results.get("processed_image_filename"):
                response_data["overlay_image_url"] = f"/media/results/{results['processed_image_filename']}"
                
            return response_data
        except Exception:
            if path.exists():
                try:
                    os.remove(path)
                except Exception:
                    pass
            raise
    
    def process_video_file(
        self,
        uploaded_file,
        skip_frames: int = 2,
        save_annotated: bool = True
    ) -> Dict:
        """
        Process uploaded video file for plate detection
        
        Returns:
            Dictionary with results and metadata
        """
        ext = os.path.splitext(uploaded_file.name)[1] or ".mp4"
        fn = f"original_video_{uuid.uuid4().hex}{ext}"
        tmp_path = self.upload_dir / fn
        try:
            with open(tmp_path, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            result = process_video(
                video_path=str(tmp_path),
                output_dir=str(self.videos_dir),
                skip_frames=skip_frames,
                save_annotated=save_annotated,
                debug_gov=False,
            )
            response_data = {
                "success": True,
                "video_info": result["video_info"],
                "detections_count": result["detections_count"],
                "unique_plates": result["unique_plates"],
                "plates_summary": result["plates_summary"],
                "timestamp": result["timestamp"],
            }
            if result.get("output_video"):
                response_data["processed_video_url"] = (
                    "/media/results/" + os.path.basename(result["output_video"])
                )
            return response_data
        except Exception:
            if tmp_path.exists():
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise


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
