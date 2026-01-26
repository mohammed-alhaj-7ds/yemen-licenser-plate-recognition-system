import { useState } from "react";
import Button from "./Button";
import "./ResultCard.css";

function ResultCard({ plate, index, overlayImageUrl, onDownloadOverlay }) {
  const [showRawReads, setShowRawReads] = useState(false);
  const [showDebug, setShowDebug] = useState(false);

  const getPlateTypeLabel = (type) => {
    if (!type || String(type).toLowerCase() === "unknown") return "غير متوفر";
    const types = {
      private: "خصوصي",
      commercial: "نقل",
      taxi: "أجرة",
      government: "حكومي",
      temporary: "مؤقت",
    };
    return types[String(type).toLowerCase()] || "غير متوفر";
  };

  const getPlateColorLabel = (color) => {
    if (!color || String(color).toLowerCase() === "unknown") return "غير متوفر";
    const colors = {
      blue: "أزرق",
      yellow: "أصفر",
      white: "أبيض",
      red: "أحمر",
    };
    return colors[String(color).toLowerCase()] || "غير متوفر";
  };

  const fmt = (v) => {
    if (
      v === undefined ||
      v === null ||
      v === "" ||
      String(v).toLowerCase() === "unknown"
    )
      return null;
    return v;
  };

  const getConfidenceTooltip = (type) => {
    if (type === "detection") {
      return "دقة نموذج YOLOv8 في اكتشاف وجود اللوحة في الصورة";
    }
    return "دقة محرك EasyOCR في قراءة النص من اللوحة";
  };

  const ocr = plate.ocr_confidence != null ? plate.ocr_confidence : 0;
  const badge =
    ocr >= 0.8
      ? { label: "موثوق", icon: "✅", className: "badge-trusted" }
      : ocr >= 0.5
        ? { label: "يحتاج مراجعة", icon: "⚠️", className: "badge-review" }
        : { label: "ضعيف", icon: "❌", className: "badge-weak" };

  return (
    <div className="result-card">
      <div className="result-section result-section-badges">
        <span
          className={`confidence-badge ${badge.className}`}
          title="حسب دقة القراءة OCR"
        >
          {badge.icon} {badge.label}
        </span>
      </div>

      {/* License Plate Information */}
      <div className="result-section">
        <h3 className="section-title">
          <span className="section-icon">📋</span>
          License Plate Information
        </h3>
        <div className="plate-info-grid plate-info-grid-ordered">
          <div className="info-item">
            <span className="info-label">
              <span className="info-icon">📍</span>
              Governorate
            </span>
            <span className="info-value">
              {fmt(plate.governorate_name) ?? fmt(plate.governorate) ?? (
                <span className="not-available">ℹ️ Unknown</span>
              )}
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">
              <span className="info-icon">🔢</span>
              Governorate Code
            </span>
            <span className="info-value">
              {fmt(plate.governorate_code) ?? (
                <span className="not-available">ℹ️ N/A</span>
              )}
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">
              <span className="info-icon">🚙</span>
              Vehicle Type
            </span>
            <span className="info-value">
              {(() => {
                const vType = plate.vehicle_type || plate.plate_type;
                if (!vType || String(vType).toLowerCase() === "unknown")
                  return "N/A";
                const types = {
                  car: "Car",
                  pickup: "Pickup",
                  truck: "Truck",
                  vehicle: "Vehicle",
                };
                return types[String(vType).toLowerCase()] || vType;
              })()}
            </span>
          </div>

          <div className="info-item">
            <span className="info-label">
              <span className="info-icon">🎨</span>
              Plate Color
            </span>
            <span className="info-value">
              {getPlateColorLabel(plate.plate_color)}
            </span>
          </div>
        </div>
      </div>

      {/* Confidence Metrics */}
      <div className="result-section">
        <h3 className="section-title">
          <span className="section-icon">📊</span>
          Confidence Metrics
        </h3>
        <div className="confidence-section">
          <div className="confidence-item">
            <div className="confidence-header">
              <div className="confidence-label-group">
                <span className="confidence-label">Detection Accuracy</span>
                <span
                  className="confidence-tooltip"
                  title={getConfidenceTooltip("detection")}
                >
                  ℹ️
                </span>
              </div>
              <span className="confidence-percentage">
                {plate.detection_confidence != null ? (
                  `${(plate.detection_confidence * 100).toFixed(1)}%`
                ) : (
                  <span className="not-available">ℹ️ غير متوفر</span>
                )}
              </span>
            </div>
            <div className="confidence-bar">
              <div
                className="confidence-fill detection"
                style={{
                  width: `${((plate.detection_confidence || 0) * 100).toFixed(1)}%`,
                  minWidth: plate.detection_confidence ? "2%" : "0%",
                }}
              />
            </div>
          </div>

          <div className="confidence-item">
            <div className="confidence-header">
              <div className="confidence-label-group">
                <span className="confidence-label">OCR Accuracy</span>
                <span
                  className="confidence-tooltip"
                  title={getConfidenceTooltip("ocr")}
                >
                  ℹ️
                </span>
              </div>
              <span className="confidence-percentage">
                {plate.ocr_confidence != null ? (
                  `${(plate.ocr_confidence * 100).toFixed(1)}%`
                ) : (
                  <span className="not-available">ℹ️ غير متوفر</span>
                )}
              </span>
            </div>
            <div className="confidence-bar">
              <div
                className="confidence-fill ocr"
                style={{
                  width: `${((plate.ocr_confidence || 0) * 100).toFixed(1)}%`,
                  minWidth: plate.ocr_confidence ? "2%" : "0%",
                }}
              />
            </div>
          </div>

          {/* Vehicle Detection Confidence */}
          {plate.vehicle_confidence != null && (
            <div className="confidence-item">
              <div className="confidence-header">
                <div className="confidence-label-group">
                  <span className="confidence-label">Vehicle Detection</span>
                  <span
                    className="confidence-tooltip"
                    title="YOLOv8 model accuracy in detecting the vehicle"
                  >
                    ℹ️
                  </span>
                </div>
                <span className="confidence-percentage">
                  {`${(plate.vehicle_confidence * 100).toFixed(1)}%`}
                </span>
              </div>
              <div className="confidence-bar">
                <div
                  className="confidence-fill vehicle"
                  style={{
                    width: `${((plate.vehicle_confidence || 0) * 100).toFixed(1)}%`,
                    minWidth: plate.vehicle_confidence ? "2%" : "0%",
                  }}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Segmentation Quality (if available) */}
      {plate.segmentation_quality != null && (
        <div className="result-section">
          <h3 className="section-title">
            <span className="section-icon">🎯</span>
            Vehicle Segmentation Quality
          </h3>
          <div className="confidence-section">
            <div className="confidence-item">
              <div className="confidence-header">
                <div className="confidence-label-group">
                  <span className="confidence-label">
                    Segmentation Accuracy
                  </span>
                  <span
                    className="confidence-tooltip"
                    title="Measures how well the AI model segmented the vehicle from the background. High quality means precise vehicle boundary detection."
                  >
                    ℹ️
                  </span>
                </div>
                <span className="confidence-percentage">
                  {`${(plate.segmentation_quality * 100).toFixed(1)}%`}
                </span>
              </div>
              <div className="confidence-bar">
                <div
                  className={`confidence-fill segmentation ${plate.segmentation_class || "medium"}`}
                  style={{
                    width: `${((plate.segmentation_quality || 0) * 100).toFixed(1)}%`,
                    minWidth: plate.segmentation_quality ? "2%" : "0%",
                  }}
                />
              </div>
              {plate.segmentation_class && (
                <div className="segmentation-badge-container">
                  <span
                    className={`segmentation-badge badge-${plate.segmentation_class}`}
                  >
                    {plate.segmentation_class === "high" && "✅ High Quality"}
                    {plate.segmentation_class === "medium" &&
                      "⚠️ Medium Quality"}
                    {plate.segmentation_class === "low" && "❌ Low Quality"}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Action Buttons */}
      {overlayImageUrl && (
        <div className="result-section">
          <div className="action-buttons">
            <Button
              variant="secondary"
              size="medium"
              onClick={onDownloadOverlay}
              icon="⬇️"
            >
              Download Processed Image
            </Button>
          </div>
        </div>
      )}

      {/* Technical Details */}
      {plate.debug_info && (
        <div className="result-section">
          <button
            className="debug-toggle"
            onClick={() => setShowDebug(!showDebug)}
          >
            <span>{showDebug ? "🔼" : "🔽"}</span>
            Technical Details
          </button>
          {showDebug && (
            <div className="debug-content">
              {plate.debug_info.detection_model && (
                <div className="debug-item">
                  <span>Detection Model:</span>
                  <strong>{plate.debug_info.detection_model}</strong>
                </div>
              )}
              {plate.debug_info.ocr_engine && (
                <div className="debug-item">
                  <span>OCR Engine:</span>
                  <strong>{plate.debug_info.ocr_engine}</strong>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Raw OCR Reads */}
      {plate.raw_reads && plate.raw_reads.length > 0 && (
        <div className="result-section">
          <button
            className="raw-reads-toggle"
            onClick={() => setShowRawReads(!showRawReads)}
          >
            <span>{showRawReads ? "🔼" : "🔽"}</span>
            View Raw OCR Reads ({plate.raw_reads.length})
          </button>
          {showRawReads && (
            <div className="raw-reads-list">
              {plate.raw_reads
                .filter((r) => r && r.digits && r.digits.length >= 3)
                .slice(0, 20)
                .map((read, idx) => (
                  <div key={idx} className="raw-read-item">
                    <span className="raw-read-text">
                      {read.digits || read.raw_text || "N/A"}
                    </span>
                    <span className="raw-read-conf">
                      {read.confidence != null
                        ? `${(read.confidence * 100).toFixed(0)}%`
                        : "—"}
                    </span>
                    <span className="raw-read-variant">
                      {read.variant || read.source || "—"}
                    </span>
                  </div>
                ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ResultCard;
