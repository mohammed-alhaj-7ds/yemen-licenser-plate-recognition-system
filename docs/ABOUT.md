# 🚗 About Yemen ALPR Platform

## Vision

Yemen ALPR is a professional-grade Automatic License Plate Recognition platform designed for reliable vehicle identification in Yemeni environments.

---

## Problem Statement

Traditional vehicle identification systems face challenges:

- **Manual data entry** leads to errors and delays
- **Varying plate formats** require adaptable recognition
- **Lighting conditions** affect detection accuracy
- **Governorate extraction** from plate codes is essential

---

## Solution

Our multi-model AI pipeline provides:

| Stage | Technology | Purpose                             |
| ----- | ---------- | ----------------------------------- |
| 1     | YOLOv8-Seg | Vehicle segmentation and cropping   |
| 2     | YOLOv8     | License plate detection             |
| 3     | EasyOCR    | Text recognition (Arabic + English) |
| 4     | Custom     | Governorate code extraction         |

### Key Features

- ✅ 96.6% mAP detection accuracy
- ✅ Real-time image & video processing
- ✅ GPU acceleration with CPU fallback
- ✅ Production-ready Docker deployment
- ✅ RESTful API with full documentation

---

## Technology Stack

- **Backend**: Django 4.2+ / Django REST Framework
- **AI Models**: YOLOv8 (Ultralytics) + EasyOCR
- **Frontend**: React 18 + Vite
- **Deployment**: Docker + Docker Compose + Nginx

---

## Team

| Name           | Role                   |
| -------------- | ---------------------- |
| [اسم الطالب 1] | Team Lead / Full Stack |
| [اسم الطالب 2] | Backend Developer      |
| [اسم الطالب 3] | Frontend Developer     |
| [اسم الطالب 4] | ML Engineer            |

---

## Academic Context

**Course**: Computer Vision  
**Institution**: [اسم الجامعة]  
**Supervisor**: [اسم الدكتور المشرف]

---

## Privacy Note

- Uploaded images are processed and temporarily stored
- Data is automatically deleted after 24 hours
- No personal information is collected
- API access is controlled via authentication

---

## Contact

For questions or collaboration, contact the team.
