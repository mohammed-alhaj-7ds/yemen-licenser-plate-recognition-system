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

# Install minimal system dependencies (libgl1 for OpenCV stability)
# Using --no-install-recommends to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY config/ ./config/

# Copy built frontend from Stage 1
COPY --from=frontend-builder /app/frontend/dist /app/backend/staticfiles/
COPY --from=frontend-builder /app/frontend/dist /app/backend/templates/

# Create necessary directories
RUN mkdir -p ai/models media/uploads media/results media/crops static

# Set working directory to backend
WORKDIR /app/backend

# Collect static files
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Expose port (Documentation only, Railway overrides this)
EXPOSE 8000

# Health check (Pure Python, fast, no AI loading)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://0.0.0.0:{port}/api/v1/health/')" || exit 1

# Run with gunicorn using the PORT environment variable strictly
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 300 --access-logfile - --error-logfile -"]
