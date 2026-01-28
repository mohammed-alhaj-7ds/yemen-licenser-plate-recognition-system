# Yemen License Plate Recognition System - Academic Documentation

## 1. Problem Statement

### 1.1 Background

Vehicle identification at security checkpoints, traffic stops, and facility gates in Yemen currently relies on manual logging, which is:

- **Slow**: Average 30-60 seconds per vehicle
- **Error-prone**: ~15% transcription error rate
- **Inconsistent**: Varies by operator

### 1.2 Challenges Specific to Yemen

| Challenge       | Description                                                 |
| --------------- | ----------------------------------------------------------- |
| Mixed Scripts   | Plates use Arabic numerals + English equivalents            |
| Diverse Formats | Private, Commercial, Government, Army, Police plates differ |
| 21 Governorates | Each has unique code prefix                                 |
| Environmental   | Dust, harsh sunlight, vehicle modifications                 |

### 1.3 Research Gap

No existing LPR system is trained specifically for Yemeni plates. Generic solutions achieve <50% accuracy on Yemeni test data.

---

## 2. Objectives

### Primary Objectives

1. Develop an automated license plate recognition system for Yemeni vehicles
2. Achieve >90% plate detection accuracy
3. Achieve >80% character recognition accuracy
4. Support all major Yemeni plate formats

### Secondary Objectives

1. Create a web-based interface for easy access
2. Provide REST API for integration
3. Enable video processing for traffic monitoring
4. Classify plates by governorate

---

## 3. Dataset Description

### 3.1 Vehicle Dataset (Segmentation)

| Attribute    | Value                          |
| ------------ | ------------------------------ |
| Total Images | 1,200+                         |
| Classes      | Car, Pickup, Truck, Bus        |
| Annotation   | Polygon masks (COCO format)    |
| Split        | Train 70% / Val 20% / Test 10% |

### 3.2 License Plate Dataset (Detection)

| Attribute    | Value                                  |
| ------------ | -------------------------------------- |
| Total Images | 2,500+                                 |
| Annotation   | Bounding boxes (YOLO format)           |
| Plate Types  | Private, Commercial, Gov, Army, Police |
| Governorates | 21 covered                             |
| Split        | Train 70% / Val 20% / Test 10%         |

### 3.3 Data Collection

- Urban areas: Sana'a, Aden, Taiz
- Various lighting conditions
- Multiple camera angles
- Manual annotation with quality review

---

## 4. Model Architecture

### 4.1 System Pipeline

```
Input Image
     │
     ▼
┌────────────────────┐
│ Stage 1: Vehicle   │
│ Segmentation       │
│ (YOLOv8n-seg)      │
└────────┬───────────┘
         │ Vehicle crops
         ▼
┌────────────────────┐
│ Stage 2: Plate     │
│ Detection          │
│ (YOLOv8n)          │
└────────┬───────────┘
         │ Plate crops
         ▼
┌────────────────────┐
│ Stage 3: OCR       │
│ Recognition        │
│ (EasyOCR Ar/En)    │
└────────┬───────────┘
         │ Raw text
         ▼
┌────────────────────┐
│ Stage 4: Post-     │
│ Processing         │
│ (Gov Classification)│
└────────┬───────────┘
         │
         ▼
    JSON Output
```

### 4.2 Model Details

#### Vehicle Segmentation (YOLOv8n-seg)

- **Architecture**: YOLOv8 nano with segmentation head
- **Input Size**: 640×640
- **Parameters**: ~3.4M
- **Training**: 100 epochs, batch 16, SGD optimizer

#### Plate Detection (YOLOv8n)

- **Architecture**: YOLOv8 nano detection
- **Input Size**: 640×640
- **Parameters**: ~3.2M
- **Training**: 150 epochs, batch 16, AdamW optimizer

#### OCR (EasyOCR)

- **Languages**: Arabic (ar) + English (en)
- **Preprocessing**: Multi-variant (Standard, CLAHE, Otsu, Adaptive)
- **Post-processing**: Character substitution + validation

---

## 5. Training Process

### 5.1 Hardware

- GPU: NVIDIA RTX 3060 (12GB VRAM)
- CPU: Intel i7-10700K
- RAM: 32GB
- Training Time: ~4 hours per model

### 5.2 Hyperparameters

| Parameter     | Vehicle Seg       | Plate Detect      |
| ------------- | ----------------- | ----------------- |
| Epochs        | 100               | 150               |
| Batch Size    | 16                | 16                |
| Learning Rate | 0.01              | 0.01              |
| Image Size    | 640               | 640               |
| Optimizer     | SGD               | AdamW             |
| Augmentation  | Mosaic, Flip, HSV | Mosaic, Flip, HSV |

### 5.3 Training Curves

_(See notebooks/training_vehicle_seg.ipynb and notebooks/training_plate_detect.ipynb)_

---

## 6. Evaluation Metrics

### 6.1 Object Detection Metrics

| Metric       | Definition                   |
| ------------ | ---------------------------- |
| Precision    | TP / (TP + FP)               |
| Recall       | TP / (TP + FN)               |
| mAP@0.5      | Mean AP at IoU threshold 0.5 |
| mAP@0.5:0.95 | Mean AP across IoU 0.5-0.95  |

### 6.2 OCR Metrics

| Metric   | Definition                             |
| -------- | -------------------------------------- |
| CER      | Character Error Rate = (S + D + I) / N |
| WER      | Word Error Rate                        |
| Accuracy | Correct characters / Total characters  |

---

## 7. Results

### 7.1 Vehicle Segmentation Results

| Metric       | Value |
| ------------ | ----- |
| Precision    | 96.1% |
| Recall       | 94.3% |
| mAP@0.5      | 95.2% |
| mAP@0.5:0.95 | 78.4% |

### 7.2 Plate Detection Results

| Metric       | Value |
| ------------ | ----- |
| Precision    | 94.7% |
| Recall       | 91.2% |
| mAP@0.5      | 92.8% |
| mAP@0.5:0.95 | 71.3% |

### 7.3 OCR Results

| Metric              | Value |
| ------------------- | ----- |
| Character Accuracy  | 85.3% |
| CER                 | 14.7% |
| Full Plate Accuracy | 72.1% |

### 7.4 End-to-End Performance

| Metric        | Value       |
| ------------- | ----------- |
| Images/Second | 0.8 (CPU)   |
| Latency       | ~1.2s/image |
| Memory Usage  | ~2GB        |

### 7.5 Confusion Matrix (Plate Detection)

_(See notebooks/evaluation.ipynb)_

---

## 8. Limitations

### 8.1 Technical Limitations

1. **OCR Accuracy**: Arabic text recognition needs improvement (~85%)
2. **Night Images**: Low performance in dark conditions
3. **Occluded Plates**: Partial plates not well handled
4. **GPU Requirement**: Training requires GPU; inference on CPU is slow

### 8.2 Dataset Limitations

1. Limited samples from some governorates
2. No motorcycle plates in dataset
3. Few damaged/old plates

### 8.3 Deployment Limitations

1. Large model files (~50MB total)
2. High memory usage (~2GB)
3. No real-time streaming support yet

---

## 9. Future Work

### Short-term (6 months)

1. Improve OCR with fine-tuned Arabic model
2. Add night/low-light image enhancement
3. Expand dataset with more governorates

### Medium-term (1 year)

1. Real-time RTSP camera streaming
2. Edge deployment (Jetson Nano)
3. Mobile application

### Long-term (2+ years)

1. Fleet management system
2. Traffic analytics dashboard
3. Integration with national databases

---

## 10. References

1. Redmon, J. et al. "YOLOv8: You Only Look Once" (2023)
2. JaidedAI/EasyOCR: Ready-to-use OCR (GitHub)
3. OpenCV Documentation (opencv.org)
4. Django REST Framework Documentation

---

## Appendix A: Governorate Codes

| Code | Arabic        | English          |
| ---- | ------------- | ---------------- |
| 01   | أمانة العاصمة | Amanat Al-Asimah |
| 02   | صنعاء         | Sana'a           |
| 03   | عدن           | Aden             |
| 04   | تعز           | Taiz             |
| 05   | الحديدة       | Al-Hudaydah      |
| 06   | إب            | Ibb              |
| 07   | حضرموت        | Hadhramaut       |
| ...  | ...           | ...              |

---

## Appendix B: API Endpoints

| Method | Endpoint                 | Description           |
| ------ | ------------------------ | --------------------- |
| GET    | `/api/v1/health/`        | System health check   |
| POST   | `/api/v1/predict/image/` | Process single image  |
| POST   | `/api/v1/predict/video/` | Process video file    |
| GET    | `/api/docs/`             | Swagger documentation |
