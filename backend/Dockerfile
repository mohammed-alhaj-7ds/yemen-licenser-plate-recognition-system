FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY . /app/
RUN mkdir -p /app/media/uploads /app/media/results /app/media/crops /app/backend/staticfiles /app/output/logs /app/ai/models

WORKDIR /app/backend
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=core.settings.production

RUN python manage.py collectstatic --noinput 2>/dev/null || true

RUN chmod +x /app/backend/entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/app/backend/entrypoint.sh"]
