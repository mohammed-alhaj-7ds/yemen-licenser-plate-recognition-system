"""
YOLOv8-Seg Vehicle Segmentation Inference (Singleton).
Load model once; segment vehicles and crop by mask.
"""
from pathlib import Path
import cv2
import numpy as np

_SEG_MODEL = None


def _model_path() -> Path:
    repo = Path(__file__).resolve().parents[1]
    candidates = [
        Path(__file__).resolve().parent / "models" / "vehicle_segmentation.pt",
        Path(__file__).resolve().parent / "models" / "best.pt",
        Path(__file__).resolve().parent / "best.pt",
        repo / "model" / "vehicle_segmentation.pt",
        repo / "models" / "vehicle_segmentation.pt",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "YOLOv8-Seg model not found. Add ai/models/vehicle_segmentation.pt or ai/best.pt."
    )


def get_seg_model():
    """Load YOLOv8-Seg model once (singleton) with CUDA fallback."""
    global _SEG_MODEL
    if _SEG_MODEL is not None:
        return _SEG_MODEL
    
    from ultralytics import YOLO
    import torch
    
    path = _model_path()
    try:
        model = YOLO(str(path))
        
        # device selection with fallback
        if torch.cuda.is_available():
            try:
                model.to("cuda")
                print(f"Vehicle Seg Model loaded on CUDA: {path}")
            except Exception as e:
                print(f"CUDA load failed, falling back to CPU: {e}")
                model.to("cpu")
        else:
            model.to("cpu")
            print(f"Vehicle Seg Model loaded on CPU: {path}")
            
        _SEG_MODEL = model
        return _SEG_MODEL
    except Exception as e:
        print(f"CRITICAL ERROR loading Vehicle Seg Model: {e}")
        # Return None or raise? pipeline should handle it. 
        # Raising is better to detect configuration issues early, 
        # but requirements say "Do not fail request". 
        # However, without model we can't segment. 
        raise e


def segment_vehicles(img_bgr, conf=0.4):
    """
    Run YOLOv8-Seg on image. Return list of (crop_bgr, mask, bbox_xyxy, conf, vehicle_type).
    crop_bgr: vehicle cropped using mask (rest blacked out or masked region only).
    bbox_xyxy: [x1,y1,x2,y2] in image coords.
    vehicle_type: "car", "pickup", "truck", or "vehicle" (default).
    
    Returns:
        List of tuples: (crop, mask_binary, bbox, conf, vehicle_type, seg_metrics)
        where seg_metrics = {
            "mask_area": int,
            "bbox_area": int,
            "coverage_ratio": float,
            "quality": str  # "high", "medium", "low"
        }
    """
    model = get_seg_model()
    h, w = img_bgr.shape[:2]
    results = model.predict(source=img_bgr, device="cpu", conf=conf, verbose=False)
    out = []
    if not results:
        return out
    r = results[0]
    
    # Get class names from model if available
    class_names = getattr(model, 'names', {})
    
    def _get_vehicle_type(box, class_names):
        """Determine vehicle type from detection class."""
        if hasattr(box, 'cls') and box.cls is not None:
            cls_id = int(box.cls[0].cpu().numpy())
            class_name = class_names.get(cls_id, "").lower()
            if "car" in class_name or "sedan" in class_name:
                return "car"
            elif "pickup" in class_name or "pick-up" in class_name:
                return "pickup"
            elif "truck" in class_name:
                return "truck"
        # Default based on aspect ratio
        return "vehicle"
    
    def _calculate_segmentation_metrics(mask_binary, bbox):
        """Calculate segmentation quality metrics."""
        x1, y1, x2, y2 = bbox
        bbox_area = (x2 - x1) * (y2 - y1)
        
        if mask_binary is not None:
            # Calculate mask area within bbox
            mask_roi = mask_binary[y1:y2, x1:x2]
            mask_area = int(np.sum(mask_roi > 0))
        else:
            mask_area = 0
        
        # Calculate coverage ratio
        coverage_ratio = mask_area / bbox_area if bbox_area > 0 else 0.0
        
        # Classify quality
        if coverage_ratio >= 0.85:
            quality = "high"
        elif coverage_ratio >= 0.65:
            quality = "medium"
        else:
            quality = "low"
        
        return {
            "mask_area": mask_area,
            "bbox_area": bbox_area,
            "coverage_ratio": round(float(coverage_ratio), 4),
            "quality": quality
        }
    
    if r.masks is None:
        boxes = r.boxes
        if boxes is None:
            return out
        for i, box in enumerate(boxes):
            xyxy = box.xyxy[0].cpu().numpy()
            x1, y1, x2, y2 = map(int, xyxy[:4])
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            crop = img_bgr[y1:y2, x1:x2].copy()
            if crop.size == 0:
                continue
            vehicle_type = _get_vehicle_type(box, class_names)
            seg_metrics = _calculate_segmentation_metrics(None, [x1, y1, x2, y2])
            out.append((crop, None, [x1, y1, x2, y2], float(box.conf[0]), vehicle_type, seg_metrics))
        return out
    masks = r.masks
    boxes = r.boxes
    if boxes is None:
        return out
    for i, box in enumerate(boxes):
        xyxy = box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = map(int, xyxy[:4])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        mask_binary = None
        if i < len(masks.data):
            mask_data = masks.data[i].cpu().numpy()
            mask_img = cv2.resize(
                mask_data, (w, h), interpolation=cv2.INTER_LINEAR
            )
            mask_binary = (mask_img > 0.5).astype(np.uint8)
            masked = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_binary)
            crop = masked[y1:y2, x1:x2].copy()
        else:
            crop = img_bgr[y1:y2, x1:x2].copy()
        if crop.size == 0:
            continue
        conf_val = float(box.conf[0])
        vehicle_type = _get_vehicle_type(box, class_names)
        seg_metrics = _calculate_segmentation_metrics(mask_binary, [x1, y1, x2, y2])
        out.append((crop, mask_binary, [x1, y1, x2, y2], conf_val, vehicle_type, seg_metrics))
    return out
