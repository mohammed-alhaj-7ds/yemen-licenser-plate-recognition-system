import { useState, useCallback } from 'react';
import Button from './Button';
import './UploadCard.css';

function UploadCard({ onFileSelect, selectedFile, onRemove, activeTab, onTabChange }) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  }, [onFileSelect]);

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      onFileSelect(file);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="upload-card-container">
      {/* Tab Selection */}
      <div className="upload-tabs">
        <button
          className={`upload-tab ${activeTab === 'image' ? 'active' : ''}`}
          onClick={() => onTabChange('image')}
        >
          <span className="tab-icon">🖼️</span>
          تحليل صورة
        </button>
        <button
          className={`upload-tab ${activeTab === 'video' ? 'active' : ''}`}
          onClick={() => onTabChange('video')}
        >
          <span className="tab-icon">🎬</span>
          تحليل فيديو
        </button>
      </div>

      {/* Upload Card */}
      <div className="upload-card">
        {!selectedFile ? (
          <div
            className={`drop-zone ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => {
              const inputId = activeTab === 'image' ? 'fileInput' : 'fileInputVideo';
              document.getElementById(inputId)?.click();
            }}
          >
            <div className="drop-zone-icon">
              {activeTab === 'image' ? '📷' : '🎥'}
            </div>
            <h3 className="drop-zone-title">اسحب الملف هنا أو انقر للاختيار</h3>
            <p className="drop-zone-subtitle">
              {activeTab === 'image'
                ? 'يدعم: JPG, PNG, WebP (حتى 100MB)'
                : 'يدعم: MP4, AVI, MOV (حتى 500MB)'}
            </p>
            <input
              id="fileInput"
              type="file"
              className="file-input-hidden"
              accept={activeTab === 'image' ? 'image/*' : 'video/*'}
              onChange={handleFileInput}
            />
            <input
              id="fileInputVideo"
              type="file"
              className="file-input-hidden"
              accept={activeTab === 'video' ? 'video/*' : 'image/*'}
              onChange={handleFileInput}
            />
          </div>
        ) : (
          <div className="selected-file-card">
            <div className="selected-file-info">
              <span className="file-icon">
                {activeTab === 'image' ? '🖼️' : '🎬'}
              </span>
              <div className="file-details">
                <div className="file-name">{selectedFile.name}</div>
                <div className="file-size">{formatFileSize(selectedFile.size)}</div>
              </div>
            </div>
            <Button
              variant="ghost"
              size="small"
              onClick={onRemove}
              icon="❌"
            >
              إزالة
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

export default UploadCard;
