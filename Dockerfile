# =============================================
# Yemen LPR - Final Production Dockerfile
# =============================================

# --- Stage 1: Frontend Builder ---
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

# Install dependencies (cached)
COPY frontend/package*.json ./
RUN npm ci --production=false

# Copy source
COPY frontend/ ./

# Build control (Defaul: true)
ARG BUILD_FRONTEND=true
ENV BUILD_FRONTEND=${BUILD_FRONTEND}

# Build or create empty dist if skipped
RUN if [ "$BUILD_FRONTEND" = "true" ]; then \
      npm run build; \
    else \
      mkdir -p dist; \
    fi

# --- Stage 2: Backend Runtime ---
FROM python:3.11-slim

# Build Arguments
ARG BUILD_FRONTEND=true

# Environment
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Minimal Runtime Dependencies
# ✅ libgl1/libglib2.0-0: Required for OpenCV
# ✅ ffmpeg: Required for video processing
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libgl1 \
       libglib2.0-0 \
       ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python Deps
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Code
COPY backend/ ./backend/
COPY config/ ./config/
COPY ai/ ./ai/

# Copy Frontend Artifacts (if built) to Django static directory
# This allows 'collectstatic' to pick them up later
COPY --from=frontend-builder /app/frontend/dist/ ./backend/static/
COPY --from=frontend-builder /app/frontend/dist/index.html ./backend/templates/index.html

# Copy AI Models if they exist locally (for convenience, though volume preferred)
COPY ai/models/ ./ai/models/ 2>/dev/null || true

WORKDIR /app/backend

# Collect Static Files
# We accept failure in case of configuration miss as it might be handled at runtime in some setups
# But for production image, we try to collect.
RUN python manage.py collectstatic --noinput

# Expose Port
EXPOSE $PORT

# Start Command
# Using shell form to allow variable expansion of $PORT
CMD gunicorn core.wsgi:application -b 0.0.0.0:${PORT:-8080} --workers 3 --timeout 300
