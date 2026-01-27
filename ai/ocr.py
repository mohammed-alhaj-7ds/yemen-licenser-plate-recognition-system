"""
OCR module for license plate recognition
Uses EasyOCR with Arabic and English support
"""

import re
import cv2
import easyocr

# Initialize reader (lazy loading)
_reader = None

def get_reader():
    """Get or create EasyOCR reader (singleton)"""
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(['ar', 'en'], gpu=False)
    return _reader

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

def substitute_chars(text):
    """Substitute common OCR misreadings"""
    for old_char, new_char in CHAR_SUBSTITUTIONS.items():
        text = text.replace(old_char, new_char)
    return text

def extract_digits(text):
    """Extract only digits from text"""
    text = convert_arabic_digits(text)
    text = substitute_chars(text)
    digits = re.findall(r'\d', text)
    return ''.join(digits)

def read_text(image, lang=['ar', 'en']):
    """
    Read text from plate image using EasyOCR
    
    Args:
        image: Grayscale or BGR image
        lang: Languages to use
    
    Returns:
        Tuple of (text, confidence)
    """
    if image is None or image.size == 0:
        return "", 0.0
    
    reader = get_reader()
    
    # Convert to RGB for EasyOCR
    if len(image.shape) == 2:
        rgb_img = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    try:
        results = reader.readtext(rgb_img, detail=1, paragraph=False)
        
        all_texts = []
        max_conf = 0.0
        
        for bbox, text, conf in results:
            if text and len(text.strip()) > 0:
                cleaned = text.strip()
                digits = extract_digits(cleaned)
                
                if digits and len(digits) >= 2:
                    all_texts.append((digits, float(conf)))
                    if conf > max_conf:
                        max_conf = conf
        
        if all_texts:
            # Sort by length and confidence, prefer 5-6 digit results
            all_texts.sort(key=lambda x: (
                2.0 if 5 <= len(x[0]) <= 6 else 1.0,
                len(x[0]),
                x[1]
            ), reverse=True)
            return all_texts[0][0], all_texts[0][1]
        
    except Exception as e:
        pass
    
    return "", 0.0

def is_valid_yemeni_plate(plate_number):
    """
    Validate if a plate number could be a valid Yemeni plate
    
    Args:
        plate_number: String to validate
    
    Returns:
        Boolean indicating validity
    """
    if not plate_number:
        return False
    
    # Clean the plate number
    cleaned = re.sub(r'[^A-Z0-9\u0621-\u06FF]', '', plate_number.upper())
    
    # Valid patterns for Yemeni plates
    valid_patterns = [
        r'^[A-Z]{1,3}\d{3,6}$',      # Letters followed by 3-6 digits
        r'^\d{3,8}$',                 # 3-8 digits only (most common)
        r'^\d{1,2}[A-Z]{1,3}\d{2,4}$', # Number-letter-number pattern
        r'^[A-Z]\d{3,5}[A-Z]$',       # Letter-digit-letter pattern
    ]
    
    return any(re.match(pattern, cleaned) for pattern in valid_patterns)

def multi_pass_ocr(image, variants=None):
    """
    Perform multi-pass OCR with different preprocessing
    
    Args:
        image: Input image
        variants: List of preprocessing variants to try
    
    Returns:
        Tuple of (best_text, confidence, all_reads)
    """
    if variants is None:
        variants = ['standard', 'otsu', 'adaptive']
    
    all_reads = []
    best_result = ("", 0.0)
    
    for variant in variants:
        try:
            # Preprocess based on variant
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
            
            if variant == 'otsu':
                _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            elif variant == 'adaptive':
                processed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                  cv2.THRESH_BINARY, 11, 2)
            else:
                processed = gray
            
            text, conf = read_text(processed)
            
            if text:
                all_reads.append({
                    'text': text,
                    'confidence': conf,
                    'variant': variant
                })
                
                if conf > best_result[1]:
                    best_result = (text, conf)
                    
        except Exception:
            continue
    
    return best_result[0], best_result[1], all_reads
