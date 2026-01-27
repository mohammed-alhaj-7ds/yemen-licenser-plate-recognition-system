# 🔌 API Documentation - Yemen ALPR

Complete API reference for the Yemen License Plate Recognition system.

---

## Base URL

```
http://localhost:8000/api/v1/
```

---

## Authentication

Include API key in header:

```
X-API-Key: your-api-key-here
```

> **Note**: API key is optional in development mode.

---

## Endpoints

### Health Check

```http
GET /api/v1/health/
```

**Response:**

```json
{
  "status": "ok",
  "timestamp": "2026-01-26T12:00:00Z",
  "model_loaded": true
}
```

---

### Image Prediction

```http
POST /api/v1/predict/image/
Content-Type: multipart/form-data
```

**Parameters:**

| Parameter | Type    | Required | Description                              |
| --------- | ------- | -------- | ---------------------------------------- |
| file      | File    | Yes      | Image file (JPG, PNG, WebP)              |
| overlay   | Boolean | No       | Generate annotated image (default: true) |

**Response Schema:**

```json
{
  "success": true,
  "results": [
    {
      "plate_number": "52470",
      "raw_ocr": "52470",
      "detection_confidence": 0.88,
      "ocr_confidence": 0.75,
      "governorate_code": "1",
      "governorate_name": "أمانة العاصمة",
      "vehicle_type": "car",
      "vehicle_confidence": 0.92,
      "bbox": [100, 200, 300, 250],
      "timestamp": "2026-01-26T12:00:00Z"
    }
  ],
  "plates_found": 1,
  "overlay_image_url": "http://localhost:8000/media/results/overlay_xxx.png"
}
```

---

### Video Prediction

```http
POST /api/v1/predict/video/
Content-Type: multipart/form-data
```

**Parameters:**

| Parameter   | Type    | Required | Description                          |
| ----------- | ------- | -------- | ------------------------------------ |
| file        | File    | Yes      | Video file (MP4, AVI, MOV)           |
| skip_frames | Integer | No       | Process every nth frame (default: 2) |

**Response:**

```json
{
  "success": true,
  "video_info": {
    "total_frames": 1000,
    "processed_frames": 500,
    "fps": 30,
    "resolution": "1920x1080"
  },
  "unique_plates": 3,
  "detections_count": 45,
  "plates_summary": [...],
  "processed_video_url": "http://localhost:8000/media/results/processed_xxx.mp4"
}
```

---

### Create API Key

```http
POST /api/v1/api-keys/create/
Content-Type: application/json
```

**Request:**

```json
{
  "name": "My API Key"
}
```

**Response:**

```json
{
  "success": true,
  "api_key": "yemen_lpr_xxxxxxxxxxxx",
  "key_id": 1,
  "created_at": "2026-01-26T12:00:00Z"
}
```

---

## Code Examples

### cURL

```bash
curl -X POST http://localhost:8000/api/v1/predict/image/ \
  -H "X-API-Key: your-key" \
  -F "file=@car.jpg" \
  -F "overlay=true"
```

### Python

```python
import requests

with open('car.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/v1/predict/image/',
        files={'file': f},
        data={'overlay': 'true'},
        headers={'X-API-Key': 'your-key'}
    )
    result = response.json()
    print(f"Plate: {result['results'][0]['plate_number']}")
```

### JavaScript

```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);
formData.append("overlay", "true");

const response = await fetch("/api/v1/predict/image/", {
  method: "POST",
  headers: { "X-API-Key": "your-key" },
  body: formData,
});

const data = await response.json();
console.log(data.results[0].plate_number);
```

---

## Error Codes

| Code | Description                                |
| ---- | ------------------------------------------ |
| 400  | Bad Request - Invalid file or parameters   |
| 401  | Unauthorized - Invalid or missing API key  |
| 413  | Payload Too Large - File exceeds limit     |
| 422  | Unprocessable Entity - Invalid file format |
| 429  | Too Many Requests - Rate limit exceeded    |
| 500  | Internal Server Error                      |

---

## Rate Limits

- **Image**: 100 requests/minute
- **Video**: 10 requests/minute
- **Max file size**: 50MB (image), 500MB (video)
- **Timeout**: 60 seconds
