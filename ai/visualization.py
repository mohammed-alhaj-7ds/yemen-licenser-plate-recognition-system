import cv2
import numpy as np

def draw_detections(image, vehicles, plates):
    """
    Draw bounding boxes, labels, and segmentation masks for vehicles and plates.
    
    Args:
        image: cv2 image (BGR)
        vehicles: list of vehicle dicts {
            bbox: [x1, y1, x2, y2], 
            type: str, 
            confidence: float,
            segmentation: {quality: str, coverage_ratio: float, ...} (optional)
        }
        plates: list of plate dicts {bbox: [x1, y1, x2, y2], plate_number: str, confidence: float}
    
    Returns:
        Annotated image with segmentation overlays
    """
    annotated = image.copy()
    
    # Quality-based colors for segmentation overlay (BGR format)
    quality_colors = {
        "high": (0, 255, 0),      # Green
        "medium": (0, 255, 255),  # Yellow
        "low": (0, 0, 255)        # Red
    }
    
    # Draw vehicles with segmentation overlay
    for v in vehicles:
        bbox = v.get("bbox")
        if not bbox:
            continue
            
        x1, y1, x2, y2 = map(int, bbox)
        
        # Draw semi-transparent segmentation overlay if available
        seg_data = v.get("segmentation")
        if seg_data:
            quality = seg_data.get("quality", "low")
            overlay_color = quality_colors.get(quality, (0, 255, 0))
            
            # Create semi-transparent overlay for bbox region
            overlay = annotated.copy()
            alpha = 0.2  # Transparency level
            cv2.rectangle(overlay, (x1, y1), (x2, y2), overlay_color, -1)
            cv2.addWeighted(overlay, alpha, annotated, 1 - alpha, 0, annotated)
        
        # Draw bounding box
        box_color = (0, 255, 0)  # Green for vehicle
        cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, 2)
        
        # Prepare label
        label = f"{v.get('type', 'Vehicle')} {v.get('confidence', 0):.2f}"
        if seg_data:
            coverage = seg_data.get('coverage_ratio', 0)
            label += f" | Seg: {coverage:.0%}"
        
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        # Label background
        cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw + 10, y1), box_color, -1)
        # Text (Black)
        cv2.putText(annotated, label, (x1 + 5, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # Draw plates (Orange)
    for p in plates:
        bbox = p.get("bbox")
        if bbox:
            x1, y1, x2, y2 = map(int, bbox)
            # Orange for plate (BGR: 0, 165, 255)
            color = (0, 165, 255)
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            text = p.get("plate_number", "")
            conf = p.get("confidence", 0) or p.get("detection_confidence", 0)
            
            if text:
                label = f"{text} ({conf:.0%})"
            else:
                label = "Plate"
                
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw + 10, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 5, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
    return annotated
