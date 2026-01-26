from pathlib import Path
import os

import cv2
from ultralytics import YOLO

# Lazy-loaded YOLO model (avoid network attempts if path is wrong)
_model = None


def _resolve_model_path() -> str:
    """
    Resolve local YOLO weights path.
    Priority: ENV var > ai/models/plate_detect.pt > ai/best.pt > legacy paths
    """
    # First check ENV variable
    env_path = os.getenv("YOLO_DETECT_MODEL_PATH")
    if env_path:
        p = Path(env_path)
        if not p.is_absolute():
            # Relative to repo root
            p = Path(__file__).resolve().parents[1] / env_path
        if p.exists():
            return str(p)
    
    repo_root = Path(__file__).resolve().parents[1]  # workspace root
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
    raise FileNotFoundError(
        "YOLO weights not found. Set YOLO_DETECT_MODEL_PATH or add ai/models/plate_detect.pt. "
        + "Expected one of: " + ", ".join(str(p) for p in candidates)
    )


def get_model() -> YOLO:
    """Get or create YOLO model (singleton)."""
    global _model
    if _model is None:
        weights = _resolve_model_path()
        _model = YOLO(weights)
        _model.to("cpu")
    return _model

def detect_plates(image, conf_thres=0.4):
    """
    image: صورة BGR (numpy array)
    يرجع قائمة من العناصر: (crop_bgr, conf, bbox)
    bbox = [x1, y1, x2, y2]
    """
    # استخدم predict مع تحديد الجهاز
    model = get_model()
    results = model.predict(source=image, device="cpu")[0]
    plates = []

    if results.boxes is None:
        return plates
    for box in results.boxes:
        # xyxy قد يكون Tensor؛ نحوله لأرقام صحيحة
        xyxy = box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = map(int, xyxy[:4])
        conf = float(box.conf[0])

        if conf >= conf_thres:
            # تأكد من حدود الصورة
            h, w = image.shape[:2]
            x1c, y1c = max(0, x1), max(0, y1)
            x2c, y2c = min(w, x2), min(h, y2)
            crop = image[y1c:y2c, x1c:x2c].copy()
            if crop.size == 0:
                continue
            plates.append((crop, conf, [x1c, y1c, x2c, y2c]))

    return plates
