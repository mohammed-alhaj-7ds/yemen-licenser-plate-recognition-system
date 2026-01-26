# Yemen LPR - Presentation Outline

## Slide 1: Title

**Yemen License Plate Recognition System**

- Team/Author Name
- Institution
- Date

---

## Slide 2: Problem Statement

- Manual vehicle logging is slow and error-prone
- Yemeni plates have unique challenges:
  - Mixed Arabic/English text
  - Multiple plate types (Private, Commercial, Government)
  - Environmental noise (dust, lighting)

---

## Slide 3: Solution Overview

- AI-powered automated recognition
- Multi-stage pipeline for accuracy
- Web-based interface for easy access

---

## Slide 4: System Architecture

```
[Image/Video] → [Vehicle Seg] → [Plate Detect] → [OCR] → [Result]
```

- YOLOv8-Seg for vehicle segmentation
- YOLOv8 for plate detection
- EasyOCR for text recognition

---

## Slide 5: Technology Stack

| Layer      | Technologies            |
| ---------- | ----------------------- |
| Frontend   | React, Vite             |
| Backend    | Django, DRF             |
| AI         | YOLOv8, EasyOCR, OpenCV |
| Deployment | Railway, Docker         |

---

## Slide 6: Demo - Image Processing

1. Upload image via web interface
2. System segments vehicle
3. Detects and crops plate
4. Extracts text and governorate
5. Returns annotated result

---

## Slide 7: Demo - API Usage

```bash
curl -X POST /api/v1/predict/image/ \
  -F "image=@car.jpg"
```

Response:

```json
{
  "plates": [
    {
      "plate_number": "12345",
      "governorate": "صنعاء"
    }
  ]
}
```

---

## Slide 8: Results & Accuracy

- Vehicle Detection: >95%
- Plate Detection: >90%
- OCR Accuracy: ~85%
- Processing Time: <2s per image

---

## Slide 9: Challenges & Solutions

| Challenge        | Solution                     |
| ---------------- | ---------------------------- |
| Mixed scripts    | Multi-pass OCR with variants |
| Background noise | Two-stage segmentation       |
| Large models     | Singleton loading pattern    |

---

## Slide 10: Future Work

1. Edge deployment (Jetson Nano)
2. Real-time camera streaming
3. Fleet management dashboard
4. Mobile application

---

## Q&A

Questions?

---

## Demo Checklist

- [ ] Start backend server
- [ ] Open web interface
- [ ] Test image upload
- [ ] Show Swagger docs at `/api/docs/`
- [ ] Show health endpoint
