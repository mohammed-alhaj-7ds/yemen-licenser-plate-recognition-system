"""
Yemen LPR - Plate Detection Module
Safe model loading with graceful error handling.
"""
from pathlib import Path
import os
import logging

import cv2

logger = logging.getLogger(__name__)

# Singleton model instance
_model = None
_model_error = None


def _resolve_model_path() -> str:
    """
    Resolve YOLO plate detection weights path.
    Priority: ENV var > ai/models/plate_detect.pt > ai/best.pt > legacy paths
    Returns None if not found (instead of raising).
    """
    # First check ENV variable
    env_path = os.getenv("YOLO_DETECT_MODEL_PATH")
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            p = Path(__file__).resolve().parents[1] / env_path
        if p.exists():
            return str(p)
        logger.warning(f"YOLO_DETECT_MODEL_PATH set but file not found: {env_path}")
    
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        Path(__file__).resolve().parent / "models" / "plate_detect.pt",
        Path(__file__).resolve().parent / "models" / "best.pt",
        Path(__file__).resolve().parent / "best.pt",
        repo_root / "model" / "best.pt",
        repo_root / "models" / "best.pt",
    ]
    
    for p in candidates:
        if p.exists():
            return str(p)
    
    return None


def get_model():
    """
    Get or create YOLO model (singleton).
    Returns None if model not available (safe degradation).
    """
    global _model, _model_error
    
    if _model is not None:
        return _model
    
    if _model_error is not None:
        return None
    
    try:
        weights = _resolve_model_path()
        if weights is None:
            _model_error = "Plate detection model not found. Set YOLO_DETECT_MODEL_PATH or add ai/models/plate_detect.pt"
            logger.error(_model_error)
            return None
        
        from ultralytics import YOLO
        _model = YOLO(weights)
        _model.to("cpu")
        logger.info(f"Plate detection model loaded from: {weights}")
        return _model
        
    except Exception as e:
        _model_error = f"Failed to load plate detection model: {str(e)}"
        logger.error(_model_error)
        return None


def is_model_available() -> bool:
    """Check if model is available without loading it."""
    return _resolve_model_path() is not None


def get_model_error() -> str:
    """Get the last model loading error message."""
    return _model_error


def detect_plates(image, conf_thres=0.4):
    """
    Detect plates in image.
    Returns: list of (crop_bgr, confidence, [x1, y1, x2, y2])
    Returns empty list if model not available (graceful degradation).
    """
    model = get_model()
    if model is None:
        logger.warning("Plate detection skipped: model not available")
        return []
    
    try:
        results = model.predict(source=image, device="cpu", verbose=False)[0]
        plates = []
        
        if results.boxes is None:
            return plates
        
        h, w = image.shape[:2]
        for box in results.boxes:
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy[:4])
            conf = float(box.conf[0])
            
            if conf >= conf_thres:
                x1c, y1c = max(0, x1), max(0, y1)
                x2c, y2c = min(w, x2), min(h, y2)
                crop = image[y1c:y2c, x1c:x2c].copy()
                if crop.size == 0:
                    continue
                plates.append((crop, conf, [x1c, y1c, x2c, y2c]))
        
        return plates
        
    except Exception as e:
        logger.error(f"Plate detection failed: {str(e)}")
        return []
