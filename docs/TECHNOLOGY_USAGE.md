# استخدام التقنيات في المشروع
# Technology Usage in the Project

---

## 📌 نظرة عامة | Overview

هذا المستند يوضح أين وكيف تم استخدام كل تقنية في المشروع.

This document explains where and how each technology is used in the project.

---

## 1. CNN (Convolutional Neural Network) | الشبكة العصبية التلافيفية

### أين تم الاستخدام:
- **YOLOv8-Seg Backbone (CSPDarknet)**: استخراج الميزات من الصور

### الملفات:
- `ai/inference.py`: تحميل واستخدام YOLOv8-Seg
- `ai/pipeline.py`: استخدام النموذج في المعالجة

### كيف يعمل:
```python
# في ai/inference.py
model = YOLO('ai/models/best.pt')  # YOLOv8-Seg يحتوي على CNN
results = model.predict(source=img_bgr)  # CNN يستخرج الميزات
```

### المكونات:
- **Convolutional Layers**: استخراج الميزات (edges → shapes → objects)
- **Pooling Layers**: تقليل الأبعاد
- **Batch Normalization**: تسريع التدريب
- **Activation Functions**: ReLU, SiLU

### النتيجة:
- استخراج ميزات هرمية من الصور
- تمكين الكشف الدقيق للمركبات

---

## 2. Detection (Object Detection) | كشف الكائنات

### أين تم الاستخدام:
- **YOLOv8**: كشف لوحات الترخيص داخل المركبات

### الملفات:
- `ai/detector.py`: كشف لوحات الترخيص
- `ai/pipeline.py`: استخدام الكشف في المعالجة

### كيف يعمل:
```python
# في ai/detector.py
model = YOLO('ai/best.pt')  # نموذج YOLOv8 للكشف
results = model.predict(source=image, conf=0.4)
# النتيجة: bounding boxes (x1, y1, x2, y2) + confidence
```

### المخرجات:
- **Bounding Boxes**: إحداثيات الصندوق حول اللوحة
- **Confidence Scores**: درجة الثقة في الكشف
- **Class Labels**: نوع الكائن (license_plate)

### النتيجة:
- كشف دقيق للوحات الترخيص
- تقليل False Positives (الكشف داخل المركبة فقط)

---

## 3. Segmentation (Instance Segmentation) | التقسيم

### أين تم الاستخدام:
- **YOLOv8-Seg**: تقسيم المركبات (car, pickup, truck)

### الملفات:
- `ai/inference.py`: تقسيم المركبات
- `ai/pipeline.py`: استخدام التقسيم لقص المركبة

### كيف يعمل:
```python
# في ai/inference.py
model = YOLO('ai/models/best.pt')  # YOLOv8-Seg
results = model.predict(source=img_bgr)
masks = results[0].masks  # قناع التقسيم
# استخدام mask لقص المركبة
masked = cv2.bitwise_and(img_bgr, img_bgr, mask=mask_binary)
```

### المخرجات:
- **Masks**: قناع ثنائي (binary) لكل مركبة
- **Bounding Boxes**: صندوق حول المركبة
- **Vehicle Type**: نوع المركبة (car, pickup, truck)

### النتيجة:
- تقسيم دقيق للمركبات
- قص المركبة فقط (تقليل الضوضاء)
- كشف اللوحة داخل المركبة فقط

---

## 4. Metrics (مقاييس التقييم) | Evaluation Metrics

### أين تم الاستخدام:
- **Notebook**: `notebooks/yemen_lpr_analysis.ipynb`
- **التقرير**: `docs/ACADEMIC_REPORT.md`

### المقاييس المستخدمة:

#### 1. Precision (الدقة)
$$Precision = \frac{TP}{TP + FP}$$

- **الاستخدام**: قياس دقة الكشف
- **النتيجة**: 98.4%
- **التفسير**: من كل الكشوفات، 98.4% كانت صحيحة

#### 2. Recall (الاستدعاء)
$$Recall = \frac{TP}{TP + FN}$$

- **الاستخدام**: قياس قدرة النظام على كشف جميع المركبات
- **النتيجة**: 93.4%
- **التفسير**: من كل المركبات الموجودة، تم كشف 93.4%

#### 3. mAP@0.5 (Mean Average Precision)
- **الاستخدام**: متوسط الدقة عند IoU threshold = 0.5
- **النتيجة**: 96.6%
- **التفسير**: دقة عالية جداً في الكشف

#### 4. mAP@0.5:0.95
- **الاستخدام**: متوسط الدقة عند IoU thresholds من 0.5 إلى 0.95
- **النتيجة**: 69.4%
- **التفسير**: أداء جيد عند مستويات دقة مختلفة

### الملفات:
- `notebooks/yemen_lpr_analysis.ipynb`: عرض Metrics
- `docs/ACADEMIC_REPORT.md`: شرح Metrics

---

## 5. Pipeline الكامل | Complete Pipeline

### التدفق:

```
1. Input Image
   ↓
2. YOLOv8-Seg (CNN + Segmentation)
   - CNN: استخراج الميزات
   - Segmentation: تقسيم المركبة
   ↓
3. Crop Vehicle (using mask)
   ↓
4. YOLOv8 Detection
   - كشف لوحة الترخيص داخل المركبة
   ↓
5. EasyOCR
   - قراءة النص (عربي + إنجليزي)
   ↓
6. Governorate Extraction
   - استخراج كود المحافظة
   ↓
7. JSON Output
   - plate_number
   - detection_confidence
   - ocr_confidence
   - governorate_name
   - vehicle_type
```

### الملفات:
- `ai/pipeline.py`: Pipeline الرئيسي
- `ai/inference.py`: Segmentation
- `ai/detector.py`: Detection
- `ai/ocr.py`: OCR
- `ai/gov_detect.py`: Governorate extraction

---

## 6. ملخص الاستخدام | Usage Summary

| التقنية | الملف | الوظيفة |
|---------|-------|---------|
| **CNN** | `ai/inference.py` | استخراج الميزات في YOLOv8-Seg |
| **Detection** | `ai/detector.py` | كشف لوحات الترخيص |
| **Segmentation** | `ai/inference.py` | تقسيم المركبات |
| **Metrics** | `notebooks/yemen_lpr_analysis.ipynb` | تقييم الأداء |

---

## 7. أمثلة الكود | Code Examples

### CNN في YOLOv8-Seg:
```python
# YOLOv8-Seg يستخدم CNN تلقائياً
from ultralytics import YOLO
model = YOLO('ai/models/best.pt')  # يحتوي على CNN layers
```

### Detection:
```python
# في ai/detector.py
results = model.predict(source=image, conf=0.4)
boxes = results[0].boxes  # Bounding boxes
```

### Segmentation:
```python
# في ai/inference.py
results = model.predict(source=img_bgr)
masks = results[0].masks  # Segmentation masks
```

---

## 8. الخلاصة | Conclusion

### التقنيات المستخدمة:
1. ✅ **CNN**: في YOLOv8-Seg Backbone
2. ✅ **Detection**: كشف لوحات الترخيص
3. ✅ **Segmentation**: تقسيم المركبات
4. ✅ **Metrics**: تقييم الأداء (Precision, Recall, mAP)

### النتيجة:
نظام متكامل يستخدم جميع التقنيات المطلوبة بشكل صحيح وفعال.

---

**ملاحظة**: جميع التقنيات موثقة في:
- `notebooks/yemen_lpr_analysis.ipynb`
- `docs/ACADEMIC_REPORT.md`
- `docs/PRESENTATION.md`
