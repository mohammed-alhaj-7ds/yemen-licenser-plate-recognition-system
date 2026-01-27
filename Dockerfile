# =============================================
# Yemen LPR - Production Dockerfile (Multi-Stage)
# =============================================
# Stage 1: Build Frontend (Node.js)
# =============================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# =============================================
# Stage 2: Production Runtime (Python)
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

# Install system dependencies
# ✅ libgl1/libglib2.0-0 for OpenCV
# ✅ ffmpeg for Video processing
# ✅ build-essential for compiling heavier pip packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    build-essential \
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
# Files in /assets/ go to /app/backend/static/assets/
COPY --from=frontend-builder /app/frontend/dist/assets /app/backend/static/assets/
# Copy favicon and other root static files (excluding index.html)
COPY --from=frontend-builder /app/frontend/dist/*.svg /app/backend/static/ 2>/dev/null || true
COPY --from=frontend-builder /app/frontend/dist/*.png /app/backend/static/ 2>/dev/null || true
COPY --from=frontend-builder /app/frontend/dist/*.ico /app/backend/static/ 2>/dev/null || true

# Copy index.html to Templates folder for Django to serve
COPY --from=frontend-builder /app/frontend/dist/index.html /app/backend/templates/index.html

# Set working directory to backend
WORKDIR /app/backend

# Collect static files
# This gathers everything from STATICFILES_DIRS (backend/static) to STATIC_ROOT
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://0.0.0.0:{port}/api/v1/health/')" || exit 1

# Run with gunicorn
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --worker-class gthread --timeout 300 --access-logfile - --error-logfile -"]
