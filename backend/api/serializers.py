"""
Django REST Framework Serializers
"""
from rest_framework import serializers


class PlateResultSerializer(serializers.Serializer):
    """Serializer for plate detection results."""
    plate_number = serializers.CharField()
    raw_ocr = serializers.CharField(required=False)
    detection_confidence = serializers.FloatField()
    ocr_confidence = serializers.FloatField()
    bbox = serializers.ListField(child=serializers.IntegerField())
    crop_path = serializers.CharField(required=False, allow_null=True)
    timestamp = serializers.CharField()


class ImagePredictionResponseSerializer(serializers.Serializer):
    """Serializer for image prediction response."""
    success = serializers.BooleanField()
    results = PlateResultSerializer(many=True)
    plates_found = serializers.IntegerField()
    timestamp = serializers.CharField()
    overlay_image_url = serializers.CharField(required=False)


class VideoInfoSerializer(serializers.Serializer):
    """Serializer for video info."""
    total_frames = serializers.IntegerField()
    processed_frames = serializers.IntegerField()
    fps = serializers.IntegerField()
    resolution = serializers.CharField()


class PlateSummarySerializer(serializers.Serializer):
    """Serializer for plate summary in video."""
    plate_number = serializers.CharField()
    occurrences = serializers.IntegerField()
    max_confidence = serializers.FloatField()
    first_seen_frame = serializers.IntegerField()


class VideoPredictionResponseSerializer(serializers.Serializer):
    """Serializer for video prediction response."""
    success = serializers.BooleanField()
    video_info = VideoInfoSerializer()
    detections_count = serializers.IntegerField()
    unique_plates = serializers.IntegerField()
    plates_summary = PlateSummarySerializer(many=True)
    processed_video_url = serializers.CharField(required=False)
    timestamp = serializers.CharField()


class HealthCheckSerializer(serializers.Serializer):
    """Serializer for health check response."""
    status = serializers.CharField()
    timestamp = serializers.CharField()
    model_loaded = serializers.BooleanField()
