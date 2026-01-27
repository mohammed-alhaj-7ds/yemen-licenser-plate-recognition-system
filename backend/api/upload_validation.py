"""
Upload validation: file type and size.
"""
from django.conf import settings

MAX_IMAGE_SIZE = getattr(settings, "FILE_UPLOAD_MAX_MEMORY_SIZE", 104_857_600)
MAX_VIDEO_SIZE = 104_857_600 * 5

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov"}


def _ext(name):
    if "." not in name:
        return ""
    return "." + name.rsplit(".", 1)[-1].lower()


def validate_image_upload(uploaded_file):
    """Returns (None, None) if valid, else (error_dict, status_code)."""
    if _ext(uploaded_file.name) not in ALLOWED_IMAGE_EXTENSIONS:
        return (
            {"error": "Invalid file type", "message": "Allowed: JPG, PNG, WebP only."},
            400,
        )
    if uploaded_file.size > MAX_IMAGE_SIZE:
        return (
            {"error": "File too large", "message": f"Max size: {MAX_IMAGE_SIZE // (1024*1024)}MB."},
            413,
        )
    return None, None


def validate_video_upload(uploaded_file):
    """Returns (None, None) if valid, else (error_dict, status_code)."""
    if _ext(uploaded_file.name) not in ALLOWED_VIDEO_EXTENSIONS:
        return (
            {"error": "Invalid file type", "message": "Allowed: MP4, AVI, MOV only."},
            400,
        )
    if uploaded_file.size > MAX_VIDEO_SIZE:
        return (
            {"error": "File too large", "message": f"Max size: {MAX_VIDEO_SIZE // (1024*1024)}MB."},
            413,
        )
    return None, None
