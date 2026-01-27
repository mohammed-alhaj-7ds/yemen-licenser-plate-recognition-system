# =============================================
# Yemen LPR - Production Dockerfile (Multi-Stage)
# =============================================
# Stage 1: Build Frontend (Node.js 20 Lts)
# =============================================
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
# Copy package definitions first for caching
COPY frontend/package*.json ./
# Install deps using clean install
RUN npm ci
# Copy source and build
COPY frontend/ ./
RUN npm run build

# =============================================
# Stage 2: Production Runtime (Python 3.11 Slim)
# =============================================
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    FORCE_CPU=True \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

WORKDIR /app

# Install minimal system dependencies
# ✅ libgl1/libglib2.0-0 for OpenCV
# ✅ ffmpeg for Video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p ai/models media/uploads media/results media/crops static

# Copy built frontend Assets to Django Static folder
COPY --from=frontend-builder /app/frontend/dist/assets /app/backend/static/assets/
# Copy root static files (favicon, etc)
COPY --from=frontend-builder /app/frontend/dist/*.svg /app/backend/static/ 2>/dev/null || true
COPY --from=frontend-builder /app/frontend/dist/*.png /app/backend/static/ 2>/dev/null || true
COPY --from=frontend-builder /app/frontend/dist/*.ico /app/backend/static/ 2>/dev/null || true

# Copy index.html to Templates folder
COPY --from=frontend-builder /app/frontend/dist/index.html /app/backend/templates/index.html

# Set working directory to backend
WORKDIR /app/backend

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8000

# Health check (Pure Python, fast, zero deps)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://0.0.0.0:{port}/api/v1/health/')" || exit 1

# Run with gunicorn
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --worker-class gthread --timeout 300 --access-logfile - --error-logfile -"]
