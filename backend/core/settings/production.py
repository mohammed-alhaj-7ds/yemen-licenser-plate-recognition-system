"""
Django production settings.
"""
from .base import *  # noqa: F401, F403
print("DEBUG: Loading production.py settings...")

DEBUG = False
ALLOWED_HOSTS = ["*"]

# CORS: restrict origins in production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["https://*.railway.app"],
)
# Allow Railway domains for CSRF (POST requests)
CSRF_TRUSTED_ORIGINS = ["https://*.railway.app"]

# Logging: disable verbose/unnecessary logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"simple": {"format": "%(levelname)s %(name)s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "api": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

# Security headers (applied via middleware or Nginx)
SECURE_X_FRAME_OPTIONS = "DENY"
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
