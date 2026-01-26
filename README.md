# Yemen License Plate Recognition System (Yemen LPR)

![License](https://img.shields.io/badge/License-Proprietary-blue.svg) ![Version](https://img.shields.io/badge/Version-1.1.0-emerald.svg) ![Status](https://img.shields.io/badge/Status-Production%20Ready-violet.svg)

**A state-of-the-art, production-grade computer vision platform designed for the automated detection and recognition of Yemeni vehicle license plates.**

---

## 📋 Project Overview

Yemen LPR is a specialized machine learning system engineered to address the unique challenges of vehicle identification in Yemen. Unlike generic LPR solutions, this platform is built on a specific, localized dataset and features a robust multi-model pipeline that separates vehicle segmentation from plate detection to ensure maximum accuracy in complex urban environments.

---

## ⚠️ Real-World Problem Statement

Manual vehicle logging at security checkpoints, traffic stops, and facility gates in Yemen is currently inefficient and prone to significant human error. The specific challenges include:

- **Diverse Plate Formats**: Yemeni plates vary significantly (Private, Commercial, Government, Army, Police) with mixed Arabic/English text.
- **Environmental Noise**: Dust, harsh lighting, and unstandardized vehicle modifications make direct OCR methods unreliable.
- **Security Gaps**: The lack of automated real-time identification creates vulnerabilities in security infrastructure and delays in traffic management.

---

## 💡 Solution Overview

We have developed a **Multi-Stage AI Pipeline** that ensures reliability by breaking the problem down:

1.  **Isolate**: First, effectively segment the vehicle from the background.
2.  **Detect**: Locate the plate within the vehicle boundary.
3.  **Recognize**: innovative OCR tuned for Arabic/English mixed formats.

This logic is wrapped in a high-performance **Django REST API** and served via a modern **React** interface, creating a seamless user experience for operators and developers alike.

---

## 📂 Project Structure

The project ecosystem is designed with a clear separation of concerns between Research/Training and Production Inference.

```
├── Training & Datasets (Research Phase)
│   ├── License Plate Recognition/      # Plate Detection Training
│   │   ├── dataset/ (train/valid/test)
│   │   └── runs/detect/train/weights/
│   └── vehicle_segmentation/           # Vehicle Segmentation Training
│       ├── dataset/ (train/valid/test)
│       └── runs/segment/vehicle_seg/weights/
│
└── yemen-licenser-plate-recognition-system (Production Phase)
    ├── ai/                             # Inference Engine & Pipeline
    ├── backend/                        # Django REST API
    ├── frontend/                       # React User Interface
    └── docs/                           # Documentation
```

> **Note**: This repository contains the **Production System**. The training datasets and raw model runs are maintained in the separate Research directories to ensure the production environment remains lightweight and optimized.

---

## 🤖 AI Models Used

Our pipeline utilizes three distinct models working in harmony:

1.  **Vehicle Segmentation (YOLOv8-Seg)**
    - **Role**: Detects vehicles (cars, trucks, buses) and generates a precise segmentation mask.
    - **Benefit**: Removes background clutter (sidewalks, buildings), ensuring subsequent steps focus only on the vehicle.

2.  **License Plate Detection (YOLOv8)**
    - **Role**: Locates the license plate within the segmented vehicle crop.
    - **Benefit**: High-precision bounding boxes even for small or angled plates.

3.  **Optical Character Recognition (EasyOCR)**
    - **Role**: Reads the alphanumeric characters from the detected plate.
    - **Benefit**: Customized configuration to handle mixed Arabic/English digits and text.

---

## ⚙️ Training Pipeline Overview

During the research phase, we curated two distinct datasets:

1.  **Vehicle Dataset**: Annotated with polygon masks for instance segmentation.
2.  **Yemeni Plate Dataset**: Annotated with bounding boxes for object detection.

Models were trained independently to maximize their feature extraction capabilities before being integrated into the unified production pipeline.

---

## 🚀 Production Inference Pipeline

The runtime system executes the following flow for every request:

1.  **Input**: Image or Video Frame.
2.  **Preprocessing**: Resizing and normalization.
3.  **Stage 1 - Segmentation**: `YOLOv8-Seg` identifies vehicle instances.
4.  **Cropping**: The system crops the image to the vehicle masks.
5.  **Stage 2 - Detection**: `YOLOv8` finds plates within the vehicle crops.
6.  **Stage 3 - OCR**: `EasyOCR` extracts text from the plate region.
7.  **Post-Processing**: Logic to validate plate formats and extract governorate codes.
8.  **Output**: JSON response with structured data + overlay visualization.

---

## 🏗️ System Architecture

- **Backend**: Django 5 + Django REST Framework. Serves the API, handles authentication, and manages the AI pipeline.
- **AI Engine**: PyTorch + Ultralytics (Inference Mode). Optimized for CPU/GPU inference.
- **Frontend**: React + Vite. A responsive Single Page Application (SPA) consuming the API.

---

## 🔌 API Overview

Full documentation is available via **Swagger UI** at `/api/docs/`.

| Endpoint                 | Method | Description                  |
| :----------------------- | :----- | :--------------------------- |
| `/api/v1/predict/image/` | `POST` | Analyze a static image file. |
| `/api/v1/predict/video/` | `POST` | Process a video file.        |
| `/api/v1/api-keys/`      | `POST` | Manage authentication keys.  |
| `/api/v1/health/`        | `GET`  | System health check.         |

---

## 💻 Frontend Overview

The user interface follows a modern **Deep Navy** product theme:

- **Home/Demo**: Live interaction area for immediate testing.
- **Developers**: A professional portal with API reference and code snippets (Stripe-style).
- **Use Cases**: Real-world application scenarios.
- **Ask Assistant**: A built-in context-aware AI guide.

---

## 💬 Ask Assistant (Interactive AI)

To improve user experience, we implemented **Ask Assistant**, a context-aware floating, interactive help layer. It understands the user's current page (Home, Developers, etc.) and offers relevant suggestions, helping users navigate technical documentation or understand model capabilities without leaving the app.

---

## 📊 Dataset Description

The system performance relies on high-quality localized data:

- **Vehicles**: Diverse collection of cars, armored vehicles, buses, and trucks common in Yemen.
- **Plates**: Dataset covers all major Yemeni governorate formats, insuring coverage across Sana'a, Aden, Hadhramaut, and others.

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- (Optional) Docker Desktop

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
```

### 2. Frontend Setup

```bash
cd frontend
npm install
```

---

## ▶️ Running the Project

### Running Backend

```bash
cd backend
python manage.py runserver
# API available at http://127.0.0.1:8000
```

### Running Frontend

```bash
cd frontend
npm run dev
# UI available at http://localhost:3000
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```ini
DEBUG=True
SECRET_KEY=your-secret-key
FORCE_CPU=False  # Set to True if you don't have a CUDA GPU
YOLO_SEG_MODEL_PATH=ai/weights/yolov8n-seg.pt
YOLO_DETECT_MODEL_PATH=ai/weights/best.pt
```

---

## 📚 API Documentation

Access the interactive Swagger documentation (Redoc/Spectacular) at:
`http://localhost:8000/api/docs/`

---

## 🧪 Testing

We utilize `pytest` for endpoint integration testing.

```bash
cd backend
pytest
```

---

## 🛡️ Production Readiness

- **Security**: API Key Middleware enabled.
- **Performance**: Singleton model loading prevents memory leaks.
- **Scalability**: Stateless architecture allows container orchestration.
- **UX**: Polished, responsive, and error-tolerant interface.

---

## 🔮 Future Improvements

1.  **Edge Deployment**: Optimization for Jetson Nano/Raspberry Pi.
2.  **Real-Time Streaming**: RTMP/RTSP stream support for live cameras.
3.  **Fleet Logic**: Advanced analytics for fleet management.

---

## 📄 License

Proprietary Software. All rights reserved.
