# تقرير أكاديمي: نظام التعرف على لوحات السيارات اليمنية

# Academic Report: Yemen License Plate Recognition System

---

## 1. Introduction | المقدمة

### 1.1 Background | الخلفية

License plate recognition (LPR) systems are crucial components of intelligent transportation systems, traffic management, and security applications. In Yemen, the need for automated license plate recognition has grown significantly due to increasing vehicle numbers and the need for efficient traffic management systems.

نظم التعرف على لوحات السيارات (LPR) هي مكونات أساسية في أنظمة النقل الذكية وإدارة المرور والتطبيقات الأمنية. في اليمن، زادت الحاجة لأنظمة التعرف التلقائي على لوحات السيارات بشكل كبير بسبب زيادة عدد المركبات والحاجة لأنظمة إدارة مرور فعالة.

### 1.2 Problem Statement | بيان المشكلة

Traditional license plate recognition systems face several challenges:

- **Variability in image conditions**: Different lighting, angles, and weather conditions
- **Vehicle diversity**: Cars, pickup trucks, and commercial vehicles
- **Plate format variations**: Different plate designs and text formats
- **Arabic and English text**: Mixed language support required

### 1.3 Objectives | الأهداف

This project aims to develop a comprehensive LPR system that:

1. Accurately segments vehicles in images using deep learning
2. Detects license plates within vehicle regions
3. Recognizes Arabic and English text on plates
4. Extracts governorate information from plate numbers
5. Provides a user-friendly web interface and API

---

## 2. Problem Definition | تعريف المشكلة

### 2.1 System Requirements | متطلبات النظام

The system must:

- **Input**: Images or videos containing vehicles with Yemeni license plates
- **Processing**:
  - Vehicle segmentation (YOLOv8-Seg)
  - Plate detection (YOLOv8)
  - Text recognition (EasyOCR)
  - Governorate extraction
- **Output**: Structured JSON with plate number, confidence scores, governorate information, and metadata

### 2.2 Technical Challenges | التحديات التقنية

1. **Vehicle Segmentation**: Accurately segmenting vehicles from complex backgrounds
2. **Plate Detection**: Detecting plates within vehicle regions with high precision
3. **OCR Accuracy**: Reading mixed Arabic-English text with varying quality
4. **Governorate Mapping**: Extracting governorate code from left-side digit
5. **Real-time Processing**: Balancing accuracy and speed

---

## 3. Dataset Description | وصف Dataset

### 3.1 Vehicle Segmentation Dataset

**Source**: [Roboflow - Vehicle Segmentation](https://universe.roboflow.com/kemalkilicaslan/vehicle-segmentation-2uulk)

- **Type**: Instance Segmentation (YOLOv8 format)
- **Classes**: vehicle (car, pickup, truck)
- **Format**: Images + segmentation masks (polygon annotations)
- **Statistics**:
  - Training: ~7,000+ images
  - Validation: ~2,000+ images
  - Test: ~1,000+ images

### 3.2 Plate Detection Dataset

- **Type**: Object Detection (YOLOv8 format)
- **Classes**: license_plate
- **Model**: `ai/best.pt` (pre-trained weights)
- **Characteristics**:
  - Various plate sizes and orientations
  - Different lighting conditions
  - Mixed Arabic-English text

### 3.3 Dataset Characteristics | خصائص Dataset

- **Diversity**: Multiple vehicle types, angles, and lighting conditions
- **Quality**: High-resolution images with clear plate visibility
- **Annotations**: Accurate bounding boxes and segmentation masks
- **Format**: YOLOv8 compatible format for seamless integration

---

## 4. Methodology | المنهجية

### 4.1 System Architecture | البنية المعمارية

The system follows a multi-stage pipeline:

```
Input Image
    ↓
Vehicle Segmentation (YOLOv8-Seg)
    ↓
Crop Vehicle Region (using mask)
    ↓
Plate Detection (YOLOv8)
    ↓
OCR (EasyOCR)
    ↓
Governorate Extraction
    ↓
JSON Output
```

### 4.2 Technologies Used | التقنيات المستخدمة

1. **YOLOv8-Seg**: Vehicle instance segmentation
2. **YOLOv8**: License plate detection
3. **EasyOCR**: Optical character recognition
4. **Django**: Backend API framework
5. **React**: Frontend user interface
6. **Docker**: Containerization for deployment

---

## 5. Model Architecture (CNN + Segmentation) | البنية المعمارية للنموذج

### 5.1 YOLOv8-Seg Architecture

#### 5.1.1 Backbone: CSPDarknet

- **Convolutional Neural Network (CNN) Layers**: Extract features from input images
- **CSP (Cross Stage Partial) Blocks**: Improve gradient flow and reduce computations
- **Depth-wise Separable Convolutions**: Reduce parameters while maintaining performance

**CNN Components**:

- Convolutional layers with kernel sizes 3×3 and 1×1
- Batch Normalization for stable training
- SiLU activation function
- Residual connections (ResNet-like)

#### 5.1.2 Neck: PANet (Path Aggregation Network)

- **Feature Pyramid Network (FPN)**: Multi-scale feature fusion
- **Bottom-up Path**: Transfer features from high to low levels
- **Lateral Connections**: Connect features at the same scale

#### 5.1.3 Head: Detection + Segmentation

**Detection Head**:

- **Classification Branch**: Predicts object class (vehicle)
- **Regression Branch**: Predicts bounding box coordinates (x, y, w, h)
- **Confidence Score**: Probability of object presence

**Segmentation Head**:

- **Mask Decoder**: Generates pixel-level masks for each instance
- **Pixel Classification**: Determines if each pixel belongs to the object
- **Instance Separation**: Distinguishes between multiple objects

### 5.2 Instance Segmentation vs Other Methods

| Method                    | Output                 | Use Case                                       |
| ------------------------- | ---------------------- | ---------------------------------------------- |
| **Object Detection**      | Bounding boxes only    | Fast detection, approximate location           |
| **Semantic Segmentation** | Pixel-level classes    | Scene understanding, no instance separation    |
| **Instance Segmentation** | Bounding boxes + masks | Precise object boundaries, instance separation |

### 5.3 CNN in Segmentation

**Convolutional Layers**:

- Extract hierarchical features (edges → shapes → objects)
- Use learnable filters (kernels) to detect patterns
- Apply convolution operation: `output = conv(input, kernel) + bias`

**Pooling Layers**:

- Reduce spatial dimensions (downsampling)
- Max Pooling: Select maximum value in window
- Average Pooling: Average values in window

**Activation Functions**:

- **ReLU**: `f(x) = max(0, x)` - Introduces non-linearity
- **SiLU**: `f(x) = x * sigmoid(x)` - Smooth activation

**Skip Connections**:

- ResNet-style connections
- Help with gradient flow in deep networks
- Enable training of very deep architectures

---

## 6. Training Details | تفاصيل التدريب

### 6.1 Training Configuration

- **Model**: YOLOv8n-seg (nano variant for speed)
- **Epochs**: 50
- **Batch Size**: 16
- **Image Size**: 640×640
- **Device**: CPU (can use GPU for faster training)
- **Optimizer**: AdamW
- **Learning Rate**: 0.01 (with cosine annealing)

### 6.2 Data Augmentation

- **Horizontal Flip**: Random horizontal flipping
- **Rotation**: Random rotation (±10 degrees)
- **Brightness/Contrast**: Random adjustments
- **Scale**: Random scaling
- **Mosaic**: Combine 4 images into one

### 6.3 Loss Functions

1. **Box Loss**: Measures bounding box prediction error
   - Uses IoU (Intersection over Union) metric
   - Penalizes incorrect box coordinates

2. **Segmentation Loss**: Measures mask prediction error
   - Binary cross-entropy for pixel classification
   - Dice loss for mask overlap

3. **Classification Loss**: Measures class prediction error
   - Cross-entropy loss
   - Focal loss for hard examples

**Total Loss**: Weighted sum of all three losses

---

## 7. Evaluation Metrics | مقاييس التقييم

### 7.1 Precision (الدقة)

$$Precision = \frac{TP}{TP + FP}$$

- **TP (True Positives)**: Correctly detected vehicles
- **FP (False Positives)**: Incorrectly detected (not vehicles)
- **Meaning**: Of all detections, how many were correct?

**Result**: 98.4%

### 7.2 Recall (الاستدعاء)

$$Recall = \frac{TP}{TP + FN}$$

- **FN (False Negatives)**: Vehicles present but not detected
- **Meaning**: Of all vehicles present, how many were detected?

**Result**: 93.4%

### 7.3 mAP@0.5 (Mean Average Precision at IoU=0.5)

**IoU (Intersection over Union)**:
$$IoU = \frac{Area\ of\ Overlap}{Area\ of\ Union}$$

- Measures overlap between predicted and ground-truth boxes
- IoU = 0.5 means 50% overlap required

**AP (Average Precision)**:

- Average of precision values at different recall levels
- Area under Precision-Recall curve

**mAP@0.5**: Mean AP across all classes at IoU threshold = 0.5

**Result**: 96.6%

### 7.4 mAP@0.5:0.95

- Average AP at IoU thresholds from 0.5 to 0.95 (step 0.05)
- More stringent metric requiring higher localization accuracy
- Tests model performance at various overlap levels

**Result**: 69.4%

### 7.5 Summary of Results

| Metric           | Value | Interpretation                          |
| ---------------- | ----- | --------------------------------------- |
| **mAP@0.5**      | 96.6% | Excellent detection accuracy            |
| **Precision**    | 98.4% | Very few false positives                |
| **Recall**       | 93.4% | Most vehicles detected                  |
| **mAP@0.5:0.95** | 69.4% | Good localization at various IoU levels |

---

## 8. Results | النتائج

### 8.1 Segmentation Performance

The YOLOv8-Seg model successfully:

- Segments vehicles with high accuracy (96.6% mAP@0.5)
- Generates precise masks for vehicle boundaries
- Handles various vehicle types (cars, pickups, trucks)
- Works under different lighting and angle conditions

### 8.2 Plate Detection Performance

- Detects plates within vehicle regions with high confidence
- Reduces false positives by searching only in vehicle crops
- Handles plates at various angles and sizes

### 8.3 OCR Performance

- Reads Arabic and English text accurately
- Handles Arabic-Indic digit conversion (٠١٢ → 012)
- Multi-pass OCR with different preprocessing improves accuracy

### 8.4 Governorate Extraction

- Successfully extracts left-side digit for governorate code
- Maps codes to governorate names using lookup table
- Handles cases where extraction fails gracefully

### 8.5 Interactive Assistant Layer

An embedded conversational assistant was implemented to enhance user experience, reduce the learning curve, and guide users through system usage, APIs, and real-world applications. This aligns with modern human-centered AI system design principles, providing context-aware support and reducing the cognitive load on developers and end-users.

### 8.6 System Integration

- **Backend API**: Django REST Framework provides robust API
- **Frontend**: React interface with modern UI/UX
- **Docker**: Containerized deployment for easy setup
- **Performance**: Processes images in seconds

---

## 9. Limitations | القيود

### 9.1 Dataset Limitations

- **General Dataset**: Vehicle segmentation dataset is general, not Yemen-specific
- **Plate Dataset**: Limited Yemeni plate examples in training
- **Diversity**: May not cover all plate variations in Yemen

### 9.2 Technical Limitations

1. **Image Quality**: Performance degrades with:
   - Blurry or low-resolution images
   - Extreme lighting conditions
   - Heavy occlusion

2. **Angle Dependency**:
   - Side angles may reduce OCR accuracy
   - Extreme angles may fail detection

3. **Governorate Extraction**:
   - Relies on single left-side digit
   - May fail if digit is unclear or missing

4. **Processing Speed**:
   - CPU processing is slower than GPU
   - Large images take more time

### 9.3 Future Improvements

1. **Fine-tuning**: Train on Yemen-specific vehicle and plate data
2. **Data Augmentation**: Increase dataset diversity
3. **GPU Acceleration**: Use GPU for faster inference
4. **Post-processing**: Improve OCR results with validation rules
5. **Real-time Processing**: Optimize for video stream processing

---

## 10. Conclusion | الخاتمة

### 10.1 Summary

This project successfully developed a comprehensive Yemen License Plate Recognition system using:

- **YOLOv8-Seg** for vehicle instance segmentation (CNN-based)
- **YOLOv8** for license plate detection
- **EasyOCR** for text recognition
- **Django + React** for web interface and API

### 10.2 Key Achievements

1. **High Accuracy**: 96.6% mAP@0.5 for vehicle segmentation
2. **Robust Pipeline**: Multi-stage processing ensures reliable results
3. **User-Friendly**: Modern web interface and comprehensive API
4. **Production-Ready**: Docker deployment and proper error handling

### 10.3 Technical Contributions

- Demonstrated effective use of CNN for feature extraction
- Applied instance segmentation for precise vehicle boundaries
- Integrated multiple deep learning models in a unified pipeline
- Developed end-to-end system from research to deployment

### 10.4 Applications

- **Traffic Management**: Automated vehicle tracking and monitoring
- **Security Systems**: Access control and surveillance
- **Parking Management**: Automated parking systems
- **Law Enforcement**: Vehicle identification and tracking

### 10.5 Future Work

- Fine-tune models on Yemen-specific data
- Support additional plate types and formats
- Implement real-time video processing
- Add vehicle type classification
- Improve governorate extraction accuracy

---

## References | المراجع

1. Ultralytics YOLOv8 Documentation: https://docs.ultralytics.com/
2. EasyOCR Documentation: https://github.com/JaidedAI/EasyOCR
3. Roboflow Vehicle Segmentation Dataset: https://universe.roboflow.com/kemalkilicaslan/vehicle-segmentation-2uulk
4. Django REST Framework: https://www.django-rest-framework.org/
5. React Documentation: https://react.dev/

---

## Appendix | الملاحق

### A. System Architecture Diagram

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Image/    │────▶│  YOLOv8-Seg  │────▶│    Crop     │
│   Frame     │     │  (CNN + Seg) │     │   Vehicle   │
└─────────────┘     └──────────────┘     └─────────────┘
                                               │
                    ┌──────────────┐            │
                    │    JSON      │◀───────────┤
                    │   Output     │            │
                    └──────────────┘            ▼
                           ▲           ┌─────────────┐
                           │           │  YOLOv8     │
                    ┌──────────────┐   │  Detection  │
                    │  Governorate │   └─────────────┘
                    │  Extraction  │            │
                    └──────────────┘            ▼
                           ▲           ┌─────────────┐
                           └───────────│   EasyOCR   │
                                       │  AR + EN    │
                                       └─────────────┘
```

### B. Technology Stack

| Component            | Technology   | Purpose                         |
| -------------------- | ------------ | ------------------------------- |
| Vehicle Segmentation | YOLOv8-Seg   | CNN-based instance segmentation |
| Plate Detection      | YOLOv8       | Object detection                |
| OCR                  | EasyOCR      | Text recognition                |
| Backend              | Django + DRF | API server                      |
| Frontend             | React + Vite | Web interface                   |
| Deployment           | Docker       | Containerization                |

### C. Metrics Explanation

- **CNN**: Convolutional Neural Network - Deep learning architecture for image processing
- **Detection**: Identifying objects and their locations (bounding boxes)
- **Segmentation**: Pixel-level classification (masks)
- **Metrics**: Quantitative measures of model performance

---

**Report Prepared By**: [Your Name]  
**Date**: January 2026  
**Course**: Computer Vision  
**Institution**: [Your University]
