# Backend Dockerfile - Production Ready for Railway
# CPU-only, no CUDA, works with Railway/Render/Fly.io

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FORCE_CPU=True

# Install system dependencies (OpenCV requirements)
# Using libgl1 instead of libgl1-mesa-glx for modern Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY config/ ./config/
COPY media/ ./media/

# Create necessary directories
RUN mkdir -p ai/models media/uploads media/results media/crops static

# Set working directory to backend
WORKDIR /app/backend

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Run with gunicorn (PORT comes from Railway)
CMD gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 120
