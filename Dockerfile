# =============================================
# Yemen LPR - Production Dockerfile (Multi-Stage)
# =============================================
# Stage 1: Build Frontend (Node.js)
# =============================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
# Copy dependency definitions
COPY frontend/package*.json ./
# Install deps (ci is faster/cleaner than install)
RUN npm ci
# Copy source and build
COPY frontend/ ./
RUN npm run build

# =============================================
# Stage 2: Production Runtime (Python)
# =============================================
# ❌ NO apt-get
# ❌ NO libgl, mesa, x11
# ✅ Pure Python dependencies
# ✅ Railway/Docker compatible
# ✅ CPU-only inference
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

# Copy requirements first
COPY backend/requirements.txt ./requirements.txt

# Install Python dependencies only (no system packages)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY config/ ./config/

# Copy built frontend from Stage 1
# Using a specific static location that Django can find
COPY --from=frontend-builder /app/frontend/dist /app/backend/staticfiles/
COPY --from=frontend-builder /app/frontend/dist /app/backend/templates/

# Create necessary directories
RUN mkdir -p ai/models media/uploads media/results media/crops static

# Set working directory to backend
WORKDIR /app/backend

# Collect static files (Unified)
# We handle errors gracefully in case of config mismatch
RUN python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Expose port
EXPOSE 8000

# Health check (Pure Python)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.environ.get('PORT', '8000'); urllib.request.urlopen(f'http://localhost:{port}/api/v1/health/')" || exit 1

# Run with gunicorn
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 120 --access-logfile - --error-logfile -"]
