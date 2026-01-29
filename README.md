# Yemen License Plate Recognition System

<div align="center">

![Version](https://img.shields.io/badge/Version-1.1.0-emerald.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-violet.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-Academic-orange.svg)

**نظام التعرف على لوحات السيارات اليمنية**

_A production-grade AI system for automated detection and recognition of Yemeni vehicle license plates._

</div>

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Problem Statement](#-problem-statement)
- [Solution Architecture](#-solution-architecture)
- [AI Models](#-ai-models)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Running Locally](#-running-locally)
- [Deployment (Railway)](#-deployment-railway)
- [API Documentation](#-api-documentation)
- [Model Files](#-model-files)
- [Academic Documentation](#-academic-documentation)
- [Team](#-team)

---

## 🎯 Project Overview

Yemen LPR is a specialized machine learning system for automated vehicle license plate recognition in Yemen. The system handles the unique challenges of Yemeni plates including:

- **Mixed Scripts**: Arabic and English characters/numerals
- **Multiple Plate Types**: Private, Commercial, Government, Army, Police
- **21 Governorates**: Automatic governorate detection

### Key Features

- ✅ Multi-stage AI pipeline (Segmentation → Detection → OCR)
- ✅ Support for images and videos
- ✅ REST API with Swagger documentation
- ✅ Modern React web interface
- ✅ Governorate classification
- ✅ Production-ready deployment

---

## ⚠️ Problem Statement

Manual vehicle logging at security checkpoints in Yemen faces critical challenges:

| Challenge                            | Impact                          |
| ------------------------------------ | ------------------------------- |
| Mixed Arabic/English text            | OCR accuracy issues             |
| Diverse plate formats                | No single detection model works |
| Environmental noise (dust, lighting) | False positives                 |
| Manual transcription                 | Human errors, delays            |

---

## 🏗️ Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                    React + Vite (Frontend)                      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/REST
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO REST API                            │
│              /api/v1/predict/image/  /api/v1/predict/video/     │
│              /api/v1/health/         /api/docs/                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     AI PIPELINE                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   YOLOv8     │  │   YOLOv8     │  │   EasyOCR    │          │
│  │   -Seg       │──▶│  Detector   │──▶│   Reader     │          │
│  │  (Vehicle)   │  │   (Plate)    │  │ (Ar/En)      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                              │                   │
│                                              ▼                   │
│                                    ┌──────────────┐             │
│                                    │ Governorate  │             │
│                                    │ Classifier   │             │
│                                    └──────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Models

### 1. Vehicle Segmentation (YOLOv8-Seg)

- **Purpose**: Isolate vehicles from background
- **Output**: Segmentation mask
- **Benefit**: Removes environmental noise

### 2. Plate Detection (YOLOv8)

- **Purpose**: Locate license plate in vehicle crop
- **Output**: Bounding box coordinates
- **Benefit**: High precision on small/angled plates

### 3. OCR Recognition (EasyOCR)

- **Purpose**: Read plate characters
- **Languages**: Arabic + English
- **Preprocessing**: Multi-pass with CLAHE, Otsu, Adaptive

### Performance Metrics

| Model                | Metric             | Value     |
| -------------------- | ------------------ | --------- |
| Vehicle Segmentation | mAP@0.5            | 95.2%     |
| Plate Detection      | mAP@0.5            | 92.8%     |
| OCR                  | Character Accuracy | ~85%      |
| End-to-End           | Processing Time    | <2s/image |

---

## 📂 Project Structure

```
yemen-lpr/
├── ai/                     # AI Pipeline
│   ├── models/             # Model weights (.pt files - NOT in Git)
│   ├── detector.py         # Plate detection
│   ├── inference.py        # Vehicle segmentation
│   ├── ocr.py              # OCR processing
│   └── pipeline.py         # Main pipeline
├── backend/                # Django REST API
│   ├── api/                # API endpoints
│   ├── core/               # Django settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # React SPA
│   ├── src/                # React components
│   └── package.json        # Node dependencies
├── notebooks/              # Academic Jupyter notebooks
├── config/                 # Configuration files
├── Dockerfile              # Production Docker build
├── Procfile                # Railway/Heroku process file
└── README.md               # This file
```

---

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Node.js 18+ (for frontend)
- Git

### Backend Setup

```bash
# Clone repository
git clone https://github.com/your-repo/yemen-lpr.git
cd yemen-lpr

# Create virtual environment
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download model files (see Model Files section)
# Place in ai/models/
```

### Frontend Setup

```bash
cd frontend
npm install
```

---

## ▶️ Running Locally

### Run Backend (API)

```bash
cd backend
python manage.py runserver
# API: http://127.0.0.1:8000
# Swagger: http://127.0.0.1:8000/api/docs/
```

### Run Frontend (Dev)

```bash
cd frontend
npm run dev
# UI: http://localhost:3000
```

### Run Both (Production-like)

```bash
# Build frontend
cd frontend && npm run build

# Run backend serving frontend
cd backend
python manage.py runserver
# Full app: http://127.0.0.1:8000
```

---

## 🚀 Deployment (Railway)

### Step 1: Prepare Repository

```bash
# Ensure .pt files are NOT committed
git status
# Should NOT show any .pt files
```

### Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository

### Step 3: Set Environment Variables

```
SECRET_KEY=your-secure-random-key
DEBUG=False
FORCE_CPU=True
DJANGO_SETTINGS_MODULE=core.settings.production
ALLOWED_HOSTS=*
```

### Step 4: Upload Model Files

**Option A: Railway Volume**

1. Create Volume in Railway dashboard
2. Mount at `/app/ai/models`
3. Upload `.pt` files via Railway CLI or SSH

**Option B: External Storage**

- Store models on S3/GCS
- Download on startup (requires code modification)

### Step 5: Deploy

Railway auto-deploys on push. Check logs for errors.

### Production URLs

| Endpoint   | URL                                               |
| ---------- | ------------------------------------------------- |
| Frontend   | `https://your-project.railway.app/`               |
| API Health | `https://your-project.railway.app/api/v1/health/` |
| Swagger    | `https://your-project.railway.app/api/docs/`      |

---

## 📚 API Documentation

### Endpoints

| Method | Endpoint                 | Description   |
| ------ | ------------------------ | ------------- |
| GET    | `/api/v1/health/`        | Health check  |
| POST   | `/api/v1/predict/image/` | Process image |
| POST   | `/api/v1/predict/video/` | Process video |
| GET    | `/api/docs/`             | Swagger UI    |

### Example Request

```bash
curl -X POST https://your-server/api/v1/predict/image/ \
  -H "X-API-Key: your-api-key" \
  -F "image=@car.jpg"
```

### Example Response

```json
{
  "success": true,
  "plates": [
    {
      "plate_number": "12345",
      "governorate": "صنعاء",
      "governorate_code": "01",
      "confidence": 0.92
    }
  ],
  "vehicles": [
    {
      "type": "car",
      "bbox": [100, 200, 400, 350]
    }
  ],
  "processed_image": "/media/results/processed_abc123.png"
}
```

---

## 📦 Model Files

### Why Not in GitHub?

Model files (`.pt`) are 20-50MB each. GitHub has file size limits and large files slow down cloning.

### Where to Get Models

1. **From Training**: Run notebooks in `notebooks/` to train
2. **From Team**: Request from project maintainers
3. **Pre-trained**: Download from releases

### Model Placement

```
ai/
└── models/
    ├── vehicle_seg.pt      # Vehicle segmentation model
    └── plate_detect.pt     # Plate detection model
```

### Environment Variables

```bash
YOLO_SEG_MODEL_PATH=ai/models/vehicle_seg.pt
YOLO_DETECT_MODEL_PATH=ai/models/plate_detect.pt
```

---

## 📖 Academic Documentation

### Key Documents

| Document                 | Purpose               |
| ------------------------ | --------------------- |
| `PROJECT_EXPLANATION.md` | Technical deep-dive   |
| `PRESENTATION.md`        | Slide content outline |
| `PROJECT_COMPLETION.md`  | Feature checklist     |
| `notebooks/`             | Training & evaluation |

### Evaluation Metrics

- **Precision**: Correctly identified plates / All detections
- **Recall**: Correctly identified plates / All actual plates
- **mAP@0.5**: Mean Average Precision at 0.5 IoU
- **CER**: Character Error Rate for OCR

---

---

---

<div align="center">

**Yemen LPR** - نظام التعرف على لوحات السيارات اليمنية

</div>
