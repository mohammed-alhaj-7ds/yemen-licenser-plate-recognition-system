"""
Yemen Vehicle License Plate Recognition & Vehicle Segmentation Pipeline.

Flow: Vehicle Seg (YOLOv8-Seg) -> Crop vehicle by mask -> Plate Detection (inside vehicle)
      -> OCR -> Governorate from left -> JSON output.
"""
import os
import sys
import cv2
import uuid
import json
import re
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai.inference import get_seg_model, segment_vehicles
from ai.gov_detect import extract_left_code_strong

_reader = None


def get_reader():
    global _reader
    if _reader is None:
        import easyocr
        _reader = easyocr.Reader(["ar", "en"], gpu=False)
    return _reader


ARABIC_DIGITS = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
}
CHAR_SUBSTITUTIONS = {
    'O': '0', 'o': '0', 'I': '1', 'l': '1', 'i': '1',
    'S': '5', 's': '5', 'B': '8', 'Z': '2', 'z': '2',
    'G': '6', 'g': '9', 'q': '9', 'A': '4', 'D': '0',
    'b': '6', 'T': '7', '|': '1'
}

CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_config(name):
    p = CONFIG_DIR / name
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def convert_arabic_digits(text):
    return "".join(ARABIC_DIGITS.get(c, c) for c in text)


def substitute_chars(text):
    for a, b in CHAR_SUBSTITUTIONS.items():
        text = text.replace(a, b)
    return text


def extract_digits_only(text):
    text = convert_arabic_digits(text)
    text = substitute_chars(text)
    return "".join(re.findall(r"\d", text))


def clean_text_for_analysis(text):
    if not text:
        return ""
    text = convert_arabic_digits(text)
    text = re.sub(r"[^0-9\u0600-\u06FF\sA-Za-z]", " ", text)
    return " ".join(text.split()).strip()


def preprocess_plate_crop(img, variant="standard"):
    if img is None or img.size == 0:
        return None
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    target_h = 100
    scale = target_h / gray.shape[0]
    nw = int(gray.shape[1] * scale)
    resized = cv2.resize(gray, (nw, target_h), interpolation=cv2.INTER_CUBIC)
    if variant == "clahe":
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return clahe.apply(resized)
    if variant == "otsu":
        _, b = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return b
    if variant == "adaptive":
        return cv2.adaptiveThreshold(
            resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    return resized


def extract_bottom_region(crop, top_ratio=0.35):
    if crop is None or crop.size == 0:
        return crop
    h = crop.shape[0]
    start = int(h * top_ratio)
    return crop[start:, :]


def extract_left_region(crop, width_ratio=0.28):
    if crop is None or crop.size == 0:
        return None
    _, w = crop.shape[:2]
    lw = int(w * width_ratio)
    return crop[:, :lw]


def multi_pass_ocr(crop, region_name="full"):
    reader = get_reader()
    candidates = []
    raw_reads = []
    variants = ["standard", "clahe", "otsu", "adaptive"]
    for v in variants:
        try:
            proc = preprocess_plate_crop(crop, v)
            if proc is None or proc.size == 0:
                continue
            if len(proc.shape) == 2:
                rgb = cv2.cvtColor(proc, cv2.COLOR_GRAY2RGB)
            else:
                rgb = cv2.cvtColor(proc, cv2.COLOR_BGR2RGB)
            results = reader.readtext(rgb, detail=1, paragraph=False)
            for _box, text, conf in results:
                if not text or not text.strip():
                    continue
                cleaned = text.strip()
                digits = extract_digits_only(cleaned)
                raw_reads.append({
                    "raw_text": cleaned, "digits": digits, "confidence": float(conf),
                    "region": region_name, "variant": v,
                    "cleaned_text": clean_text_for_analysis(cleaned),
                })
                if digits and len(digits) >= 2:
                    lb = 2.0 if 5 <= len(digits) <= 6 else 1.0
                    score = len(digits) * float(conf) * lb
                    candidates.append((digits, float(conf), score))
        except Exception:
            continue
    if not candidates:
        return "", 0.0, raw_reads
    pref = [c for c in candidates if 5 <= len(c[0]) <= 6]
    pool = pref if pref else candidates
    pool.sort(key=lambda x: x[2], reverse=True)
    best = pool[0]
    return best[0], best[1], raw_reads


def _ensure_model_loaded():
    get_seg_model()


def _plate_detector():
    from ai.detector import get_model
    return get_model()


def detect_plates_on_image(img_bgr, conf_thres=0.4):
    """Run plate detection on image (full or vehicle crop). Returns [(crop, conf, bbox)]."""
    model = _plate_detector()
    results = model.predict(source=img_bgr, device="cpu", conf=conf_thres, verbose=False)[0]
    plates = []
    h, w = img_bgr.shape[:2]
    if results.boxes is None:
        return plates
    for box in results.boxes:
        xyxy = box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = map(int, xyxy[:4])
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        crop = img_bgr[y1:y2, x1:x2].copy()
        if crop.size == 0:
            continue
        plates.append((crop, float(box.conf[0]), [x1, y1, x2, y2]))
    return plates


def process_image(
    image_path,
    save_crops=True,
    crops_dir=None,
    logs_dir=None,
    debug_gov=True,
):
    """
    Main pipeline: Vehicle Seg -> crop vehicle -> Plate Detection (inside vehicle)
    -> OCR -> Governorate from left -> JSON.
    """
    repo = Path(__file__).resolve().parent.parent
    if crops_dir is None:
        crops_dir = repo / "media" / "crops"
    if logs_dir is None:
        logs_dir = repo / "output" / "logs"
    os.makedirs(crops_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    debug_dir = str(repo / "output" / "debug_gov") if debug_gov else None

    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    import uuid
    from ai.visualization import draw_detections

    # ... (imports)

    vehicles = segment_vehicles(img, conf=0.4)
    vehicle_results = []
    plate_results = []
    
    # Track which vehicles have plates to avoid duplicates if needed, 
    # but requirement implies simply listing what's found.
    
    for vehicle_data in vehicles:
        # Handle new format with segmentation metrics
        if len(vehicle_data) == 6:
            v_crop, v_mask, v_bbox, v_conf, v_type, seg_metrics = vehicle_data
        elif len(vehicle_data) == 5:
            v_crop, v_mask, v_bbox, v_conf, v_type = vehicle_data
            seg_metrics = None
        else:
            v_crop, v_mask, v_bbox, v_conf = vehicle_data[:4]
            v_type = "vehicle"
            seg_metrics = None
        
        vx1, vy1, vx2, vy2 = v_bbox
        
        # Add to vehicle results with segmentation metrics
        vehicle_result = {
            "bbox": [vx1, vy1, vx2, vy2],
            "type": v_type,
            "confidence": float(v_conf) if v_conf else 0.0
        }
        
        # Include segmentation metrics if available
        if seg_metrics:
            vehicle_result["segmentation"] = seg_metrics
        
        vehicle_results.append(vehicle_result)

        # Plate detection on vehicle crop
        plate_detections = detect_plates_on_image(v_crop, conf_thres=0.4)

        for p_crop, p_conf, p_bbox in plate_detections:
            px1, py1, px2, py2 = p_bbox
            # Map plate bbox to original image coordinates
            bbox_orig = [
                vx1 + px1, vy1 + py1,
                vx1 + px2, vy1 + py2,
            ]
            
            crop_path = None
            if save_crops:
                fn = f"plate_{uuid.uuid4().hex[:8]}.png"
                crop_path = crops_dir / fn
                cv2.imwrite(str(crop_path), p_crop)

            bottom = extract_bottom_region(p_crop, top_ratio=0.35)
            plate_number, ocr_conf, raw_reads = multi_pass_ocr(
                bottom if bottom is not None and bottom.size > 0 else p_crop,
                "bottom_region",
            )
            gov_result = extract_left_code_strong(p_crop, debug_dir=debug_dir)

            governorate_name = gov_result.get("governorate_name") or "غير متوفر"
            governorate_code = gov_result.get("governorate_code") or ""

            res_entry = {
                "plate_number": plate_number or "",
                "raw_ocr": plate_number or "",
                "detection_confidence": round(float(p_conf), 4),
                "ocr_confidence": round(float(ocr_conf), 4),
                "governorate_name": governorate_name,
                "governorate_code": governorate_code,
                "governorate": governorate_name,
                "vehicle_type": v_type,
                "vehicle_confidence": float(v_conf) if v_conf else 0.0,
                "bbox": bbox_orig,
                "crop_path": str(crop_path) if crop_path else None,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "raw_reads": gov_result.get("raw_reads", []) + raw_reads,
                "confidence": round(float(p_conf), 4), # Mapping for viz
            }
            
            # Add segmentation quality if available
            if seg_metrics:
                res_entry["segmentation_quality"] = seg_metrics.get("coverage_ratio", 0.0)
                res_entry["segmentation_class"] = seg_metrics.get("quality", "low")
                res_entry["segmentation_details"] = seg_metrics
            
            plate_results.append(res_entry)

    # Fallback: if no vehicles found (or maybe always?), check full image for plates?
    # Logic implies: Image -> Vehicle -> Plate. 
    # If no vehicles, we might miss plates. 
    # Current code had fallback: "if not vehicles and not results: detect_plates_on_image(img)"
    # We should keep this fallback to not regress capability.
    
    if not vehicles and not plate_results:
        plate_detections = detect_plates_on_image(img, conf_thres=0.4)
        for p_crop, p_conf, p_bbox in plate_detections:
            bbox_orig = list(p_bbox)
            
            crop_path = None
            if save_crops:
                fn = f"plate_{uuid.uuid4().hex[:8]}.png"
                crop_path = crops_dir / fn
                cv2.imwrite(str(crop_path), p_crop)
                
            bottom = extract_bottom_region(p_crop, top_ratio=0.35)
            plate_number, ocr_conf, raw_reads = multi_pass_ocr(
                bottom if bottom is not None and bottom.size > 0 else p_crop,
                "bottom_region",
            )
            gov_result = extract_left_code_strong(p_crop, debug_dir=debug_dir)
            
            governorate_name = gov_result.get("governorate_name") or "غير متوفر"
            governorate_code = gov_result.get("governorate_code") or ""
            
            plate_results.append({
                "plate_number": plate_number or "",
                "raw_ocr": plate_number or "",
                "detection_confidence": round(float(p_conf), 4),
                "ocr_confidence": round(float(ocr_conf), 4),
                "governorate_name": governorate_name,
                "governorate_code": governorate_code,
                "governorate": governorate_name,
                "vehicle_type": "vehicle",
                "bbox": bbox_orig,
                "crop_path": str(crop_path) if crop_path else None,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "raw_reads": gov_result.get("raw_reads", []) + raw_reads,
                "confidence": round(float(p_conf), 4),
            })

    # Visualization
    annotated_img = draw_detections(img, vehicle_results, plate_results)
    
    # Save processed image
    processed_filename = f"processed_{uuid.uuid4().hex[:8]}.png"
    processed_path = repo / "media" / "results" / processed_filename
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(processed_path), annotated_img)

    # Consolidate response
    return {
        "vehicles": vehicle_results,
        "plates": plate_results,
        "text": " ".join([p["plate_number"] for p in plate_results if p["plate_number"]]),
        "processed_image": str(processed_path),
        "processed_image_filename": processed_filename, # Helper for services
        "confidence": {
            "vehicle": max([v["confidence"] for v in vehicle_results]) if vehicle_results else 0.0,
            "plate": max([p["detection_confidence"] for p in plate_results]) if plate_results else 0.0,
            "ocr": max([p["ocr_confidence"] for p in plate_results]) if plate_results else 0.0,
        }
    }


def process_video(
    video_path,
    output_dir,
    skip_frames=2,
    conf_threshold=0.4,
    save_annotated=True,
    debug_gov=False,
):
    from collections import defaultdict

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    os.makedirs(output_dir, exist_ok=True)
    out_path = str(Path(output_dir) / f"processed_{uuid.uuid4().hex[:8]}.mp4")
    writer = None
    if save_annotated:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(out_path, fourcc, fps, (w, h))

    debug_dir = str(Path(__file__).resolve().parent.parent / "output" / "debug_gov") if debug_gov else None
    all_detections = []
    unique_plates = defaultdict(lambda: {"count": 0, "max_conf": 0.0, "first_frame": None})
    frame_idx = 0
    processed_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
            annotated = frame.copy()
            if frame_idx % (skip_frames + 1) != 0:
                if writer:
                    writer.write(annotated)
                continue
            processed_count += 1

            vehicles = segment_vehicles(frame, conf=conf_threshold)
            for vehicle_data in vehicles:
                if len(vehicle_data) == 5:
                    v_crop, _m, v_bbox, _vc, v_type = vehicle_data
                else:
                    v_crop, _m, v_bbox, _vc = vehicle_data[:4]
                    v_type = "vehicle"
                vx1, vy1, _vx2, _vy2 = v_bbox
                plates = detect_plates_on_image(v_crop, conf_thres=conf_threshold)
                for p_crop, det_conf, p_bbox in plates:
                    px1, py1, px2, py2 = p_bbox
                    bbox = [vx1 + px1, vy1 + py1, vx1 + px2, vy1 + py2]
                    bottom = extract_bottom_region(p_crop, top_ratio=0.35)
                    plate_number, ocr_conf, _ = multi_pass_ocr(
                        bottom if bottom is not None and bottom.size > 0 else p_crop,
                        "video_bottom",
                    )
                    gov_result = extract_left_code_strong(p_crop, debug_dir=debug_dir)
                    if plate_number:
                        unique_plates[plate_number]["count"] += 1
                        unique_plates[plate_number]["max_conf"] = max(
                            unique_plates[plate_number]["max_conf"], float(det_conf)
                        )
                        if unique_plates[plate_number]["first_frame"] is None:
                            unique_plates[plate_number]["first_frame"] = frame_idx
                    all_detections.append({
                        "frame": frame_idx,
                        "plate_number": plate_number or "",
                        "raw_ocr": plate_number or "",
                        "detection_confidence": round(float(det_conf), 3),
                        "ocr_confidence": round(float(ocr_conf), 3),
                        "bbox": bbox,
                        "governorate_code": gov_result.get("governorate_code"),
                        "governorate_name": gov_result.get("governorate_name"),
                    })
                    x1, y1, x2, y2 = bbox
                    color = (0, 255, 0) if plate_number else (0, 165, 255)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    label = plate_number if plate_number else "—"
                    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw + 10, y1), color, -1)
                    cv2.putText(annotated, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            if not vehicles:
                plates = detect_plates_on_image(frame, conf_thres=conf_threshold)
                for p_crop, det_conf, bbox in plates:
                    bottom = extract_bottom_region(p_crop, top_ratio=0.35)
                    plate_number, ocr_conf, _ = multi_pass_ocr(
                        bottom if bottom is not None and bottom.size > 0 else p_crop,
                        "video_bottom",
                    )
                    gov_result = extract_left_code_strong(p_crop, debug_dir=debug_dir)
                    if plate_number:
                        unique_plates[plate_number]["count"] += 1
                        unique_plates[plate_number]["max_conf"] = max(
                            unique_plates[plate_number]["max_conf"], float(det_conf)
                        )
                        if unique_plates[plate_number]["first_frame"] is None:
                            unique_plates[plate_number]["first_frame"] = frame_idx
                    all_detections.append({
                        "frame": frame_idx,
                        "plate_number": plate_number or "",
                        "raw_ocr": plate_number or "",
                        "detection_confidence": round(float(det_conf), 3),
                        "ocr_confidence": round(float(ocr_conf), 3),
                        "bbox": bbox,
                        "governorate_code": gov_result.get("governorate_code"),
                        "governorate_name": gov_result.get("governorate_name"),
                    })
                    x1, y1, x2, y2 = bbox
                    color = (0, 255, 0) if plate_number else (0, 165, 255)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    label = plate_number if plate_number else "—"
                    (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw + 10, y1), color, -1)
                    cv2.putText(annotated, label, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            if writer:
                writer.write(annotated)
    finally:
        cap.release()
        if writer:
            writer.release()

    plates_summary = []
    for plate, info in unique_plates.items():
        plates_summary.append({
            "plate_number": plate,
            "occurrences": info["count"],
            "max_confidence": round(float(info["max_conf"]), 3),
            "first_seen_frame": info["first_frame"],
        })
    plates_summary.sort(key=lambda x: x["occurrences"], reverse=True)

    return {
        "video_info": {
            "total_frames": total_frames,
            "processed_frames": processed_count,
            "fps": fps,
            "resolution": f"{w}x{h}",
        },
        "detections_count": len(all_detections),
        "unique_plates": len(unique_plates),
        "plates_summary": plates_summary,
        "output_video": out_path if save_annotated else None,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
