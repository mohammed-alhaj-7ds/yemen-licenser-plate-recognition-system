# Production Dockerfile - Unified Full-Stack Deployment
# Builds both Frontend (React) and Backend (Django) in a single container

FROM python:3.11-slim

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install backend dependencies
COPY ./backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy and build frontend
COPY ./frontend ./frontend
WORKDIR /app/frontend
RUN npm install && npm run build

# Copy entire project
WORKDIR /app
COPY . .

# Create required directories
RUN mkdir -p media/uploads media/results media/crops ai/models static

# Collect static files
WORKDIR /app/backend
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
