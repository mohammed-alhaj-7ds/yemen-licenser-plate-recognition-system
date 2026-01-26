import { useState, useRef, useEffect } from "react";
import { useToast } from "../components/ToastContainer";
import UploadCard from "../components/UploadCard";
import PlateNumberCard from "../components/PlateNumberCard";
import ResultCard from "../components/ResultCard";
import Button from "../components/Button";
import LoadingSkeleton from "../components/LoadingSkeleton";
import { api } from "../services/api";
import "./Home.css";

function Home() {
  const [activeTab, setActiveTab] = useState("image");
  const [selectedFile, setSelectedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const { success, error: showError } = useToast();
  const resultsRef = useRef(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResults(null);
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setResults(null);
  };

  const handleAnalyze = async () => {
    if (!selectedFile || isLoading) return;

    setIsLoading(true);
    setResults(null);

    try {
      const response =
        activeTab === "image"
          ? await api.predictImage(selectedFile, true)
          : await api.predictVideo(selectedFile, 2);

      setResults(response.data);

      const platesCount =
        response.data.plates_found ?? response.data.results?.length ?? 0;
      success(
        activeTab === "image"
          ? platesCount > 0
            ? `تم العثور على ${platesCount} لوحة`
            : "تم الانتهاء من التحليل"
          : "تم معالجة الفيديو بنجاح",
      );

      setTimeout(() => {
        if (resultsRef.current) {
          resultsRef.current.scrollIntoView({
            behavior: "smooth",
            block: "start",
            inline: "nearest",
          });
        }
      }, 300);
    } catch (err) {
      // Better error messages
      let errorMessage = "حدث خطأ أثناء المعالجة";

      if (err.code === "ECONNABORTED" || err.message?.includes("timeout")) {
        errorMessage = "انتهت مهلة الاتصال. يرجى المحاولة مرة أخرى";
      } else if (err.response?.status === 400) {
        errorMessage = "الملف غير مدعوم أو تالف. يرجى اختيار ملف آخر";
      } else if (err.response?.status === 413) {
        errorMessage = "حجم الملف كبير جداً. الحد الأقصى 100MB";
      } else if (err.response?.status === 500) {
        errorMessage = "خطأ في الخادم. يرجى المحاولة لاحقاً";
      } else if (err.message) {
        errorMessage = err.message;
      }

      showError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadOverlay = (plateIndex) => {
    if (results?.overlay_image_url) {
      const link = document.createElement("a");
      link.href = results.overlay_image_url;
      link.download = `plate_result_${plateIndex + 1}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      success("تم بدء تحميل الصورة");
    }
  };

  const renderImageResults = () => {
    if (!results?.results?.length) {
      return (
        <div className="no-results">
          <div className="no-results-icon">❌</div>
          <h3>No License Plates Detected</h3>
          <p className="no-results-hint">Suggestions for better results:</p>
          <ul className="no-results-suggestions">
            <li>
              <span className="suggestion-icon">ℹ️</span> Use a clear,
              high-quality image
            </li>
            <li>
              <span className="suggestion-icon">ℹ️</span> Ensure the license
              plate is fully visible
            </li>
            <li>
              <span className="suggestion-icon">ℹ️</span> Improve lighting and
              avoid reflections
            </li>
          </ul>
        </div>
      );
    }

    return (
      <>
        <div className="results-header">
          <h3 className="results-title">
            <span className="results-icon">✅</span>
            Analysis Results ({results.plates_found || results.results.length})
          </h3>
        </div>

        {results.results.map((plate, index) => (
          <div key={index} className="plate-result-container">
            {/* بطاقة رقم اللوحة الرئيسية */}
            <PlateNumberCard plate={plate} index={index} />

            {/* بطاقة معلومات اللوحة */}
            <ResultCard
              plate={plate}
              index={index}
              overlayImageUrl={index === 0 ? results.overlay_image_url : null}
              onDownloadOverlay={() => handleDownloadOverlay(index)}
            />
          </div>
        ))}

        {results.overlay_image_url && (
          <div className="overlay-image-container">
            <h4 className="overlay-title">
              <span className="overlay-icon">🖼️</span>
              Processed Image with Detections
            </h4>
            <div className="overlay-image-wrapper">
              <img
                src={results.overlay_image_url}
                alt="Analysis Result"
                className="overlay-image"
              />
            </div>
          </div>
        )}
      </>
    );
  };

  const renderVideoResults = () => {
    if (!results) return null;

    return (
      <>
        <div className="video-summary-cards">
          <div className="summary-card">
            <div className="summary-icon">🔢</div>
            <div className="summary-content">
              <div className="summary-value">{results.unique_plates || 0}</div>
              <div className="summary-label">لوحات فريدة</div>
            </div>
          </div>
          <div className="summary-card">
            <div className="summary-icon">📊</div>
            <div className="summary-content">
              <div className="summary-value">
                {results.detections_count || 0}
              </div>
              <div className="summary-label">إجمالي الكشوفات</div>
            </div>
          </div>
          <div className="summary-card">
            <div className="summary-icon">🎬</div>
            <div className="summary-content">
              <div className="summary-value">
                {results.video_info?.processed_frames || 0}
              </div>
              <div className="summary-label">إطارات معالجة</div>
            </div>
          </div>
        </div>

        {results.plates_summary?.length > 0 && (
          <div className="plates-summary-section">
            <h3 className="section-title">اللوحات المكتشفة</h3>
            <div className="plates-list">
              {results.plates_summary.map((plate, index) => (
                <div key={index} className="plate-summary-item">
                  <div className="plate-summary-number">
                    {plate.plate_number || "غير متوفر"}
                  </div>
                  <div className="plate-summary-stats">
                    <span className="stat-item">
                      🔁 {plate.occurrences} مرة
                    </span>
                    <span className="stat-item">
                      📊 {(plate.max_confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {results.processed_video_url && (
          <div className="video-preview-container">
            <h4 className="section-title">الفيديو المعالج</h4>
            <video controls className="video-preview">
              <source src={results.processed_video_url} type="video/mp4" />
              المتصفح لا يدعم تشغيل الفيديو
            </video>
          </div>
        )}
      </>
    );
  };

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="hero-icon">🚗</span>
            AI-Powered Vehicle & License Plate Recognition
          </h1>
          <p className="hero-subtitle">
            Advanced automated detection and recognition system for vehicles and
            license plates
            <br />
            <span className="tech-stack">
              Powered by YOLOv8 Deep Learning & EasyOCR Technology
            </span>
          </p>
          <div className="hero-actions">
            <Button
              variant="primary"
              size="large"
              onClick={() => {
                const inputId =
                  activeTab === "image" ? "fileInput" : "fileInputVideo";
                document.getElementById(inputId)?.click();
              }}
              icon="▶️"
            >
              Start Analysis
            </Button>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="main-content-section">
        <div className="container">
          {/* Upload Section */}
          <div className="upload-section">
            <UploadCard
              activeTab={activeTab}
              onTabChange={setActiveTab}
              selectedFile={selectedFile}
              onFileSelect={handleFileSelect}
              onRemove={handleRemoveFile}
            />

            {selectedFile && (
              <div className="action-section">
                <Button
                  variant="primary"
                  size="large"
                  fullWidth
                  disabled={isLoading}
                  loading={isLoading}
                  loadingText="Analyzing..."
                  onClick={handleAnalyze}
                  icon="🔍"
                >
                  Start Analysis
                </Button>
              </div>
            )}
          </div>

          {/* Results Section */}
          {isLoading && (
            <div className="results-section" ref={resultsRef}>
              <LoadingSkeleton />
            </div>
          )}

          {results && !isLoading && (
            <div className="results-section" ref={resultsRef}>
              {activeTab === "image"
                ? renderImageResults()
                : renderVideoResults()}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default Home;
