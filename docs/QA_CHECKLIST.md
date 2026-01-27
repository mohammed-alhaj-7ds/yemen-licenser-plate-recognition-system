# ✅ QA Checklist - Yemen ALPR Platform

Quality assurance checklist for testing before release.

---

## 🔧 Local Development

### Backend

- [ ] `python manage.py migrate` runs without errors
- [ ] `python manage.py runserver` starts successfully
- [ ] Health endpoint returns 200: `GET /api/v1/health/`
- [ ] AI models load without CUDA errors (or fallback to CPU)

### Frontend

- [ ] `npm install` completes without errors
- [ ] `npm run dev` starts development server
- [ ] All pages load: Home, Developers, About
- [ ] No console errors in browser

---

## 📸 Image Processing

- [ ] Upload small image (<1MB) - processes in <2s
- [ ] Upload medium image (1-5MB) - processes in <5s
- [ ] Upload large image (5-50MB) - processes with progress
- [ ] Unsupported format shows error message
- [ ] File too large shows error message

### Detection Quality

- [ ] Vehicle bounding boxes appear correctly (green)
- [ ] Plate bounding boxes appear correctly (orange)
- [ ] Plate number is extracted correctly
- [ ] Governorate is identified when code is visible
- [ ] Overlay image downloads successfully

---

## 🎥 Video Processing

- [ ] Upload small video (<50MB) - processes successfully
- [ ] Progress indicator shows during processing
- [ ] Results show unique plates summary
- [ ] Processed video plays with annotations

---

## 🔌 API Testing

### cURL Tests

```bash
# Health check
curl http://localhost:8000/api/v1/health/

# Image prediction
curl -X POST http://localhost:8000/api/v1/predict/image/ \
  -F "file=@test.jpg"

# API key creation
curl -X POST http://localhost:8000/api/v1/api-keys/create/ \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'
```

### Expected Responses

- [ ] 200 OK for valid requests
- [ ] 400 Bad Request for invalid input
- [ ] JSON responses are properly formatted

---

## 🐳 Docker Deployment

- [ ] `docker-compose up --build` completes successfully
- [ ] Backend container starts and shows health OK
- [ ] Frontend container serves on port 80
- [ ] API accessible via nginx proxy
- [ ] FORCE_CPU=true works without CUDA errors

---

## 📱 Responsive Design

- [ ] Desktop (1920x1080) - Layout correct
- [ ] Tablet (768px) - Cards stack properly
- [ ] Mobile (375px) - Touch targets adequate

---

## ♿ Accessibility

- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Color contrast adequate (4.5:1 minimum)
- [ ] Alt text on images
- [ ] ARIA labels on buttons

---

## 🌐 Cross-Browser

- [ ] Chrome - All features work
- [ ] Firefox - All features work
- [ ] Safari - Basic functionality works
- [ ] Edge - All features work

---

## 🔒 Security

- [ ] API key required in production
- [ ] CORS configured correctly
- [ ] File upload size limits enforced
- [ ] No sensitive data in console logs

---

## 📊 Performance (Lighthouse)

Target scores:

- [ ] Performance: ≥ 50
- [ ] Accessibility: ≥ 85
- [ ] Best Practices: ≥ 80
- [ ] SEO: ≥ 80
