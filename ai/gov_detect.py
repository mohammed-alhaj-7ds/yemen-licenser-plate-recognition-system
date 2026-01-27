"""
Yemen License Plate Governorate Detection Utility
Handles extraction and processing of left-side governorate codes
"""

import os
import cv2
import json
import uuid
import numpy as np
from datetime import datetime
from pathlib import Path

# Arabic-Indic digits mapping
ARABIC_DIGITS = {
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
}

# Common OCR character substitutions
CHAR_SUBSTITUTIONS = {
    'O': '0', 'o': '0', 'I': '1', 'l': '1', 'i': '1',
    'S': '5', 's': '5', 'B': '8', 'Z': '2', 'z': '2',
    'G': '6', 'g': '9', 'q': '9', 'A': '4', 'D': '0',
    'b': '6', 'T': '7', '|': '1'
}

def convert_arabic_digits(text):
    """Convert Arabic-Indic digits to Western digits"""
    result = ""
    for char in text:
        result += ARABIC_DIGITS.get(char, char)
    return result

def substitute_common_chars(text):
    """Substitute common OCR misreadings"""
    for old_char, new_char in CHAR_SUBSTITUTIONS.items():
        text = text.replace(old_char, new_char)
    return text

def extract_digits_only(text):
    """Extract only digits from text"""
    text = convert_arabic_digits(text)
    text = substitute_common_chars(text)
    import re
    digits = re.findall(r'\d', text)
    return ''.join(digits)

def load_governorate_mapping():
    """Load governorate mapping from config file"""
    config_path = Path(__file__).parent.parent / 'config' / 'governorates_yemen.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback mapping
        return {
            "1": "أمانة العاصمة",
            "2": "محافظة صنعاء", 
            "3": "تعز",
            "4": "عدن",
            "5": "الحديدة",
            "6": "إب",
            "7": "ذمار",
            "8": "حضرموت",
            "9": "لحج",
            "10": "أبين",
            "11": "شبوة",
            "12": "المهرة",
            "13": "الجوف",
            "14": "مأرب",
            "15": "ريمة",
            "16": "المحويت",
            "17": "حجة",
            "18": "صعدة",
            "19": "البيضاء",
            "20": "سقطرى"
        }

def preprocess_left_region_variant(img, variant='resize_clahe'):
    """Apply specialized preprocessing for left side governorate code extraction"""
    if img is None or img.size == 0:
        return None
    
    # Convert to grayscale if needed
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    
    # Resize to standard dimensions
    target_height = 80
    target_width = 60
    resized = cv2.resize(gray, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
    
    if variant == 'resize_clahe':
        # Resize + CLAHE enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
        enhanced = clahe.apply(resized)
        return enhanced
    
    elif variant == 'adaptive_threshold':
        # Adaptive thresholding
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        enhanced = clahe.apply(resized)
        binary = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        return binary
    
    elif variant == 'bilateral_otsu':
        # Bilateral filter + OTSU thresholding
        bilateral = cv2.bilateralFilter(resized, 9, 75, 75)
        _, binary = cv2.threshold(bilateral, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary
    
    elif variant == 'invert':
        # Invert colors for better OCR on dark text
        inverted = cv2.bitwise_not(resized)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        enhanced = clahe.apply(inverted)
        return enhanced
    
    return resized

def extract_left_regions(plate_img, width_ratios=[0.22, 0.28, 0.36]):
    """Extract left side regions of plate for governorate code extraction"""
    if plate_img is None or plate_img.size == 0:
        return []
    
    h, w = plate_img.shape[:2]
    regions = []
    
    for ratio in width_ratios:
        left_width = int(w * ratio)
        # Extract left side region (full height, specified width ratio)
        left_region = plate_img[:, :left_width]
        regions.append((ratio, left_region))
    
    return regions

def extract_left_code_strong(plate_img, debug_dir=None, **kwargs):
    """
    Strong governorate code extraction from left side of plate
    
    Args:
        plate_img: Full plate image from YOLO detection
        debug_dir: Directory for debug images and JSON (optional)
    
    Returns:
        dict with governorate_code, governorate_name, governorate_source, raw_reads, debug
    """
    if plate_img is None or plate_img.size == 0:
        return {
            'governorate_code': None,
            'governorate_name': None,
            'governorate_source': None,
            'raw_reads': [],
            'debug': {
                'debug_json': None,
                'debug_images': []
            }
        }
    
    # Create debug directory if specified
    if debug_dir:
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
    else:
        timestamp = None
    
    # Extract left regions with different ratios
    width_ratios = [0.22, 0.28, 0.36]
    regions = extract_left_regions(plate_img, width_ratios)
    
    # Preprocessing variants
    variants = ['resize_clahe', 'adaptive_threshold', 'bilateral_otsu', 'invert']
    
    # Load governorate mapping
    gov_mapping = load_governorate_mapping()
    
    # Collect all OCR results
    all_raw_reads = []
    debug_images = []
    all_candidates = []
    debug_tries = []
    
    # Import EasyOCR reader
    try:
        import easyocr
        reader = easyocr.Reader(['ar', 'en'], gpu=False)
    except ImportError:
        reader = None
    
    # Process each region with each variant
    for ratio, region in regions:
        if region is None or region.size == 0:
            continue
            
        for variant in variants:
            try:
                # Apply preprocessing
                processed = preprocess_left_region_variant(region, variant)
                if processed is None or processed.size == 0:
                    continue
                
                # Save debug image if debug_dir provided
                if debug_dir and timestamp:
                    debug_filename = f"left_ratio_{ratio}_variant_{variant}_{uuid.uuid4().hex[:8]}.png"
                    debug_path = Path(debug_dir) / debug_filename
                    cv2.imwrite(str(debug_path), processed)
                    debug_images.append(str(debug_path))
                
                # EasyOCR
                ocr_results = []
                if reader:
                    try:
                        rgb_img = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
                        ocr_results = reader.readtext(rgb_img, detail=1, paragraph=False)
                    except Exception as e:
                        print(f"EasyOCR error: {e}")
                        ocr_results = []
                
                # Tesseract as fallback
                tesseract_text = None
                try:
                    import pytesseract
                    config = '--psm 7 -c tessedit_char_whitelist=0123456789'
                    tesseract_text = pytesseract.image_to_string(processed, config=config).strip()
                except:
                    pass
                
                # Process EasyOCR results
                for bbox, text, conf in ocr_results:
                    if text and len(text.strip()) > 0:
                        cleaned_text = text.strip()
                        digits_only = extract_digits_only(cleaned_text)
                        
                        # Convert to integer string to remove leading zeros
                        if digits_only and digits_only.isdigit():
                            cleaned_digits = str(int(digits_only))
                        else:
                            cleaned_digits = digits_only
                        
                        raw_read = {
                            'raw_text': cleaned_text,
                            'digits': cleaned_digits,
                            'confidence': float(conf),
                            'source': 'easyocr',
                            'region_ratio': ratio,
                            'variant': variant
                        }
                        all_raw_reads.append(raw_read)
                        
                        # الرقم الأيسر فقط: رقم واحد فقط من منطقة اليسار
                        if cleaned_digits and len(cleaned_digits) == 1 and cleaned_digits in gov_mapping:
                            score = 10 + float(conf)
                            all_candidates.append((cleaned_digits, float(conf), score, raw_read))
                
                # Process Tesseract result
                if tesseract_text:
                    tesseract_digits = extract_digits_only(tesseract_text)
                    if tesseract_digits and tesseract_digits.isdigit():
                        cleaned_tesseract = str(int(tesseract_digits))
                        
                        tesseract_read = {
                            'raw_text': tesseract_text,
                            'digits': cleaned_tesseract,
                            'confidence': 0.7,
                            'source': 'tesseract',
                            'region_ratio': ratio,
                            'variant': variant
                        }
                        all_raw_reads.append(tesseract_read)
                        
                        if len(cleaned_tesseract) == 1 and cleaned_tesseract in gov_mapping:
                            score = 10 + 0.7
                            all_candidates.append((cleaned_tesseract, 0.7, score, tesseract_read))
                
                # Record this try
                debug_tries.append({
                    'ratio': ratio,
                    'variant': variant,
                    'easyocr_results': len(ocr_results),
                    'tesseract_text': tesseract_text,
                    'debug_image': str(debug_path) if debug_dir and timestamp else None
                })
                
            except Exception as e:
                debug_tries.append({
                    'ratio': ratio,
                    'variant': variant,
                    'error': str(e)
                })
                continue
    
    # Select best candidate based on score
    best_result = None
    if all_candidates:
        all_candidates.sort(key=lambda x: x[2], reverse=True)
        best_code, best_conf, best_score, best_read = all_candidates[0]
        best_result = {
            'governorate_code': best_code,
            'governorate_name': gov_mapping[best_code],
            'governorate_source': 'local_mapping',
            'confidence': best_conf,
            'score': best_score
        }
    
    # Create debug JSON if debug_dir provided
    debug_json_path = None
    if debug_dir and timestamp:
        debug_data = {
            'timestamp': timestamp,
            'tries': debug_tries,
            'all_candidates': [
                {
                    'code': code,
                    'confidence': conf,
                    'score': score,
                    'source': read['source'],
                    'ratio': read['region_ratio'],
                    'variant': read['variant']
                }
                for code, conf, score, read in all_candidates
            ],
            'best_result': best_result,
            'total_raw_reads': len(all_raw_reads),
            'debug_images': debug_images
        }
        
        debug_json_path = Path(debug_dir) / f"debug_{timestamp}.json"
        with open(debug_json_path, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
    
    # Return result
    if best_result:
        return {
            'governorate_code': best_result['governorate_code'],
            'governorate_name': best_result['governorate_name'],
            'governorate_source': best_result['governorate_source'],
            'raw_reads': all_raw_reads,
            'debug': {
                'debug_json': str(debug_json_path) if debug_json_path else None,
                'debug_images': debug_images
            }
        }
    # المحافظة غير معروفة عند عدم إمكانية استخراج الرقم الأيسر
    return {
        'governorate_code': None,
        'governorate_name': None,
        'governorate_source': None,
        'raw_reads': all_raw_reads,
        'debug': {
            'debug_json': str(debug_json_path) if debug_json_path else None,
            'debug_images': debug_images
        }
    }