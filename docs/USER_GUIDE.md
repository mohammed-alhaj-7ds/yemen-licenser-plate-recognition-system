# 📖 User Guide - Yemen ALPR Platform

This guide explains how to use the Yemen License Plate Recognition platform.

---

## 🚀 Quick Start

### 1. Upload an Image

1. Go to the **Home** page
2. Click the upload area or drag & drop an image
3. Supported formats: JPG, PNG, WebP (max 50MB)

### 2. Analyze

1. Click **"Start Analysis"** button
2. Wait for processing (typically 1-3 seconds)
3. View results automatically

### 3. View Results

Results include:

- **Plate Number** — Detected license plate digits
- **Confidence** — Detection accuracy percentage
- **Governorate** — Extracted from left-side code
- **Vehicle Type** — Car, pickup, truck, etc.
- **Overlay Image** — Annotated image with bounding boxes

---

## 🎥 Video Processing

1. Switch to **Video** tab
2. Upload video file (MP4, AVI, MOV - max 500MB)
3. Click **Analyze**
4. View summary:
   - Total unique plates
   - Detection count per frame
   - Processed video with annotations

---

## 🔧 Model Configuration

### Using Different Models

Place `.pt` model files in `ai/models/`:

- `vehicle_segmentation.pt` — Vehicle segmentation model
- `best.pt` — Plate detection model

### CPU-Only Mode

Set `FORCE_CPU=true` in `.env` to disable GPU.

---

## ❓ Troubleshooting

| Issue              | Solution                                  |
| ------------------ | ----------------------------------------- |
| No plates detected | Use clearer image, better lighting        |
| Slow processing    | Check GPU availability, reduce image size |
| API timeout        | Increase timeout in settings              |
| Wrong governorate  | Verify plate is clearly visible           |

---

## 📞 Support

For issues, check the [Developer Documentation](/developers) or contact the team.
