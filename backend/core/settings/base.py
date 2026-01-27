"""
Django base settings — shared between dev and production.
"""
from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(str, "django-insecure-dev-only-change-in-production"),
)

# Read .env if available
environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"]) # Allow all hosts for Railway/Paas

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "api.middleware.RateLimitMiddleware",
    "api.middleware.APIKeyMiddleware",
    "api.middleware.SecurityHeadersMiddleware",
    "api.middleware.SafeExceptionMiddleware",  # Catches crash bugs
]

ROOT_URLCONF = "core.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),  # Docker production path
            os.path.join(BASE_DIR.parent, 'frontend', 'dist'),  # Local dev path
        ],
        "APP_DIRS": True,
    }
]
WSGI_APPLICATION = "core.wsgi.application"

_db_name = env("DB_PATH", default=str(BASE_DIR / "db.sqlite3"))
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": _db_name}}

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Aden"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Add frontend build assets to staticfiles dirs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent, "static"),
    os.path.join(BASE_DIR, "static"),  # Docker copies assets here
]

# Whitenoise Storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent, "media")

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# For production (Railway handles HTTPS termination, but Django should know)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

# Swagger Settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'Yemen LPR API',
    'DESCRIPTION': 'License Plate Recognition API optimized for Yemeni plates.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR', 
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Upload limits
DATA_UPLOAD_MAX_MEMORY_SIZE = 104_857_600
FILE_UPLOAD_MAX_MEMORY_SIZE = 104_857_600

# CORS
CORS_ALLOW_ALL_ORIGINS = True # For simplicity in this setup, or restrict to frontend domain
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept", "accept-encoding", "authorization", "content-type",
    "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with", "x-api-key",
]
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {"django": {"handlers": ["console"], "level": "INFO", "propagate": False}},
}

# API Config
API_RATE_LIMIT_PER_MINUTE = env.int("API_RATE_LIMIT_PER_MINUTE", default=60)
VIDEO_PROCESS_TIMEOUT_SECONDS = env.int("VIDEO_PROCESS_TIMEOUT_SECONDS", default=600)
FORCE_CPU = env.bool("FORCE_CPU", default=True) # Default to CPU for cheap deployment
