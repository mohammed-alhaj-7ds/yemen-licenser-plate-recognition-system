# Changelog — Yemen Vehicle License Plate Recognition & Vehicle Segmentation

## Version 2.0.0 — Full graduation project release

### ✅ Completed

#### AI pipeline
- **YOLOv8-Seg vehicle segmentation**: `ai/inference.py` — singleton model load, segment vehicles, crop by mask.
- **Unified pipeline** (`ai/pipeline.py`): Vehicle seg → crop vehicle → plate detection (inside vehicle) → OCR → governorate from left → JSON.
- **Model paths**: `ai/models/vehicle_segmentation.pt` (seg), `ai/best.pt` (plate detection). Fallback to `ai/best.pt` if seg model missing.
- **Plate detection** restricted to vehicle crop when vehicles are found; fallback to full-image detection.

#### Backend
- **Endpoints**: `POST /api/v1/predict/image/`, `POST /api/v1/predict/video/`, `GET /api/v1/health/`.
- **Response schema**: `plate_number`, `detection_confidence`, `ocr_confidence`, `governorate_name`, `governorate_code`, `bbox`, `overlay_image_url`, `timestamp`.
- **Storage**: Originals in `media/uploads/`, overlay in `media/results/`, crops in `media/crops/`.
- **Middleware**: API key (`X-API-Key`), rate limiting, file validation (size/type).
- **Production**: `DEBUG=False`, `STATIC_ROOT` / `MEDIA_ROOT`, Gunicorn, collectstatic.

#### Frontend
- **Home**: Upload image/video, “بدء التحليل”, loading spinner, result cards, large plate number, copy button, overlay image.
- **Developers**: API docs, endpoints, cURL / Python / JS examples, **API Playground** (upload → send → JSON), copy buttons.
- **UX**: “غير متوفر” instead of “unknown”; toasts; responsive layout.

#### Notebook
- **`notebooks/vehicle_segmentation_training.ipynb`**: Problem definition, dataset (Roboflow vehicle-segmentation), data viz, YOLOv8-Seg architecture, training code, loss curves, **metrics** (IoU, mAP50, Precision, Recall), sample predictions, discussion, conclusion.

#### Dataset & training
- **Dataset**: [Vehicle Segmentation — Roboflow](https://universe.roboflow.com/kemalkilicaslan/vehicle-segmentation-2uulk).
- **Documented**: Image counts, classes, train/val/test split in notebook.

#### Docker & deployment
- **Backend Dockerfile**: Python 3.11, deps, `ai/models` dir, collectstatic, Gunicorn.
- **Frontend Dockerfile**: Node build → Nginx.
- **docker-compose.yml**: backend + frontend, `media_data` + `backend_data` volumes.
- **Nginx**: SPA + proxy `/api/`, `/media/`, `/static/` to backend.
- **`.env.example`**: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `API_RATE_LIMIT_PER_MINUTE`, `VIDEO_PROCESS_TIMEOUT_SECONDS`, `DB_PATH`.
- **`.dockerignore`**: Excludes `*.pt` except `ai/best.pt` and `ai/models/vehicle_segmentation.pt`.

#### Documentation
- **README.md**: Local run, production, API, Docker, dataset, metrics.
- **DEPLOYMENT.md**: Docker, env, model paths, Nginx, HTTPS.
- **PROJECT_STRUCTURE.md**: Tree, pipeline, API, middleware, env.
- **CHANGELOG.md**: This file.

### 🔧 Configuration

- **New**: `ai/inference.py`, `ai/models/`, `notebooks/vehicle_segmentation_training.ipynb`.
- **Updated**: `ai/pipeline.py`, `backend/api/services.py`, `backend/api/views.py`, `backend/Dockerfile`, `.dockerignore`, `.env.example`, `DEPLOYMENT.md`, `PROJECT_STRUCTURE.md`, `CHANGELOG.md`.

### 🚀 Deployment checklist

- [x] AI pipeline (seg + plate + OCR + gov)
- [x] API endpoints and response schema
- [x] Originals, overlay, crops saved
- [x] API key, rate limit, file validation
- [x] Production settings, Gunicorn, collectstatic
- [x] Frontend SaaS-style UI, API Playground
- [x] Notebook with metrics (IoU, mAP, P, R)
- [x] Docker + docker-compose + Nginx
- [x] Docs (README, DEPLOYMENT, PROJECT_STRUCTURE, CHANGELOG)

---

**Status**: ✅ Project ready for submission and production deploy.
