"""
Django REST API Views for License Plate Recognition
Thin views layer that delegates to services
"""
from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .services import ResponseFormatter
from .models import APIKey
from .upload_validation import validate_image_upload, validate_video_upload
import secrets

DEBUG_KEYS = {"debug_info", "debug_url", "region_paths", "processing_metadata", "raw_reads"}

# Initialize formatter (safe, no AI deps)
formatter = ResponseFormatter()


def _strip_debug(data):
    if settings.DEBUG:
        return data
    if not isinstance(data, dict):
        return data
    out = {k: v for k, v in data.items() if k not in DEBUG_KEYS}
    if "results" in out and isinstance(out["results"], list):
        out["results"] = [_strip_debug(r) for r in out["results"]]
    return out


@api_view(['GET'])
def health_check(request):
    """Health check endpoint. NO AI LOADING HERE."""
    return Response(formatter.health_check(model_loaded=False))


@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict_image(request):
    """

    try:
        response_data = plate_service.process_image_file(
            uploaded_file,
            overlay=overlay,
            save_crops=True
        )
        
        if "overlay_image_url" in response_data:
            base_url = request.build_absolute_uri("/").rstrip("/")
            response_data["overlay_image_url"] = f"{base_url}{response_data['overlay_image_url']}"
        return Response(_strip_debug(response_data))
    except Exception as e:
        body, sc = formatter.error(
            str(e), "Failed to process image", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return Response(body, status=sc)


@api_view(['GET'])
def api_docs(request):
    """API Documentation Portal"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yemen LPR API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { background: #0ea5e9; color: white; padding: 2rem; border-radius: 12px; }
        .container { background: white; padding: 2rem; border-radius: 8px; margin: 2rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .endpoint { background: #f8fafc; border-left: 4px solid #0ea5e9; padding: 1.5rem; margin: 1rem 0; }
        .method { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 20px; font-weight: bold; }
        .get { background: #22c55e; color: white; }
        .post { background: #3b82f6; color: white; }
        .code-block { background: #1e293b; color: #f1f5f9; padding: 1rem; border-radius: 8px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background: #f1f5f9; font-weight: 600; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚗 Yemen License Plate Recognition API</h1>
        <p>Professional API for detecting and recognizing Yemeni license plates</p>
    </div>

    <div class="container">
        <h2>📋 Overview</h2>
        <p>This API provides professional license plate recognition for Yemeni vehicles using:</p>
        <ul>
            <li><strong>YOLOv8</strong> for vehicle detection</li>
            <li><strong>EasyOCR</strong> for character recognition</li>
            <li><strong>Perspective correction</strong> for optimal plate reading</li>
            <li><strong>Yemeni plate validation</strong> with governorate interpretation</li>
        </ul>
    </div>

    <div class="container">
        <h2>📍 API Endpoints</h2>

        <div class="endpoint">
            <span class="method get">GET</span>
            <h3>/api/v1/health/</h3>
            <p><strong>Description:</strong> Health check endpoint</p>
            <div class="code-block">
{
  "status": "ok",
  "timestamp": "2026-01-23T18:42:32.212159",
  "model_loaded": true
}
            </div>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span>
            <h3>/api/v1/predict/image/</h3>
            <p><strong>Description:</strong> Process image for license plate detection</p>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Type</th>
                    <th>Required</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>file</td>
                    <td>File</td>
                    <td>Yes</td>
                    <td>Image file (JPG, PNG, WebP)</td>
                </tr>
                <tr>
                    <td>X-API-Key</td>
                    <td>Header</td>
                    <td>Optional</td>
                    <td>API authentication key (required in production)</td>
                </tr>
                <tr>
                    <td>overlay</td>
                    <td>Boolean</td>
                    <td>No</td>
                    <td>Generate annotated image (default: true)</td>
                </tr>
            </table>
            <p><strong>Success Response (200):</strong></p>
            <div class="code-block">
{
  "success": true,
  "results": [
    {
      "plate_number": "163303",
      "raw_ocr": "163303",
      "detection_confidence": 0.85,
      "ocr_confidence": 0.78,
      "bbox": [100, 200, 300, 250],
      "crop_path": "crops/plate_0.png",
      "timestamp": "2026-01-23T18:42:32.212159",
      "governorate_code": "1",
      "governorate_name": "صنعاء",
      "car_number": "63303",
      "interpretation_confidence": 0.95
    }
  ],
  "plates_found": 1,
  "timestamp": "2026-01-23T18:42:32.212159",
  "overlay_image_url": "http://localhost:8000/media/results/result_xxxxxxxx.png"
}
            </div>
        </div>

        <div class="endpoint">
            <span class="method post">POST</span>
            <h3>/api/v1/predict/video/</h3>
            <p><strong>Description:</strong> Process video for license plate detection</p>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Type</th>
                    <th>Required</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>file</td>
                    <td>File</td>
                    <td>Yes</td>
                    <td>Video file (MP4, AVI, MOV)</td>
                </tr>
                <tr>
                    <td>X-API-Key</td>
                    <td>Header</td>
                    <td>Optional</td>
                    <td>API authentication key (required in production)</td>
                </tr>
                <tr>
                    <td>skip_frames</td>
                    <td>Integer</td>
                    <td>No</td>
                    <td>Process every nth frame (default: 2)</td>
                </tr>
            </table>
        </div>
    </div>

    <div class="container">
        <h2>🔑 API Key Management</h2>
        <p>This system uses API key authentication for security:</p>
        <ul>
            <li>During development, API key is optional</li>
            <li>In production, API key will be required for all requests</li>
            <li>API key is stored in <code>api_key.txt</code> file in the project root</li>
            <li>To use the API key, include it as an HTTP header: <code>X-API-Key: your-api-key-here</code></li>
            <li>Example with curl: <code>curl -H "X-API-Key: your-api-key" -F "file=@image.jpg" http://localhost:8000/api/v1/predict/image/</code></li>
        </ul>
    </div>

    <div class="container">
        <h2>💻 Developer Examples</h2>

        <h3>Python/Requests</h3>
        <div class="code-block">
import requests

with open('car_photo.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/predict/image/',
        files={'file': f}
    )
    
result = response.json()
if result['success']:
    plate = result['results'][0]
    print(f"Plate: {plate['plate_number']}")
    print(f"Governorate: {plate['governorate_name']}")
        </div>

        <h3>cURL</h3>
        <div class="code-block">
curl -X POST http://localhost:8000/api/v1/predict/image/ \\
  -F "file=@photo.jpg"
        </div>
    </div>

    <div class="container">
        <h2>🎯 Yemeni Plate Format Support</h2>
        <ul>
            <li>Numeric plates: 163303, 53421</li>
            <li>Letter-numeric: SA12345, A12345</li>
            <li>Numeric-letter: 12345A</li>
            <li>Minimum 2 digits, maximum 8 digits</li>
        </ul>
    </div>
</body>
</html>
    """
    return HttpResponse(html_content, content_type='text/html')


@api_view(['POST'])
@parser_classes([JSONParser])
def create_api_key(request):
    """Create a new API key for external developers. JSON body: { \"name\": \"...\" }."""
    try:
        from datetime import datetime
        
        # Generate new API key
        new_key = 'yemen_lpr_' + secrets.token_urlsafe(32)
        
        # Create API key record
        api_key_obj = APIKey.objects.create(
            key=new_key,
            name=request.data.get('name', f'API Key {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        )
        
        return Response({
            "success": True,
            "api_key": new_key,
            "key_id": api_key_obj.id,
            "created_at": api_key_obj.created_at.isoformat(),
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        err_body, status_code = formatter.error(
            f"Failed to create API key: {str(e)}",
            message=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        return Response(err_body, status=status_code)


@api_view(['POST'])
@parser_classes([MultiPartParser])
def predict_video(request):
    """
    Process a video for license plate detection.
    """
    if "file" not in request.FILES:
        body, sc = formatter.error("No file provided", "Please provide a video file in the 'file' field")
        return Response(body, status=sc)

    # Lazy import to prevent startup bottlenecks
    from .services import PlateRecognitionService
    plate_service = PlateRecognitionService()

    uploaded_file = request.FILES["file"]
    err, sc = validate_video_upload(uploaded_file)
    if err is not None:
        body, _ = formatter.error(err["error"], err.get("message", ""), sc)
        return Response(body, status=sc)

    skip_frames = int(request.data.get("skip_frames", 2))

    try:
        response_data = plate_service.process_video_file(
            uploaded_file, skip_frames=skip_frames, save_annotated=True
        )
        if "processed_video_url" in response_data:
            base_url = request.build_absolute_uri("/").rstrip("/")
            response_data["processed_video_url"] = f"{base_url}{response_data['processed_video_url']}"
        return Response(_strip_debug(response_data))
    except Exception as e:
        body, sc = formatter.error(
            str(e), "Failed to process video", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        return Response(body, status=sc)
