import { useState, useEffect } from "react";
import { useToast } from "../components/ToastContainer";
import { api } from "../services/api";
import "./Developers.css";

const API_BASE = import.meta.env.VITE_API_BASE ?? "";
const API_VERSION = "/api/v1";
const API_BASE_DISPLAY =
  API_BASE || (typeof window !== "undefined" ? window.location.origin : "");

function Developers() {
  const [apiKey, setApiKey] = useState("");
  const [isGeneratingKey, setIsGeneratingKey] = useState(false);
  const [copied, setCopied] = useState({});
  const { success, error: showError } = useToast();

  // Tab state for API Endpoints (Image / Video)
  const [activeTab, setActiveTab] = useState("image");

  useEffect(() => {
    const savedKey = localStorage.getItem("yemen_lpr_api_key");
    if (savedKey) setApiKey(savedKey);
  }, []);

  const createApiKey = async () => {
    setIsGeneratingKey(true);
    try {
      const response = await api.createApiKey(
        `Product Key ${new Date().toLocaleDateString()}`,
      );
      const newKey = response.data.api_key;
      setApiKey(newKey);
      localStorage.setItem("yemen_lpr_api_key", newKey);
      copyToClipboard(newKey, "apikey");
      success("API Key generated successfully");
    } catch (err) {
      showError("Failed to generate API Key");
    } finally {
      setIsGeneratingKey(false);
    }
  };

  const copyToClipboard = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopied((prev) => ({ ...prev, [key]: true }));
    setTimeout(() => setCopied((prev) => ({ ...prev, [key]: false })), 2000);
  };

  // Helper to get cURL example based on type
  const getCurlExample = (type) => {
    const url = `${API_BASE_DISPLAY}${API_VERSION}/predict/${type}/`;
    const key = apiKey || "YOUR_API_KEY";
    return `curl -X POST "${url}" \\
  -H "X-API-Key: ${key}" \\
  -F "file=@/path/to/${type === "image" ? "photo.jpg" : "video.mp4"}" ${type === "image" ? '\\\n  -F "overlay=true"' : ""}`;
  };

  // Helper to get JS example based on type
  const getJsExample = (type) => {
    const url = `${API_BASE_DISPLAY}${API_VERSION}/predict/${type}/`;
    const key = apiKey || "YOUR_API_KEY";
    return `const formData = new FormData();
formData.append("file", fileInput.files[0]);
${type === "image" ? 'formData.append("overlay", "true");' : ""}

const response = await fetch("${url}", {
  method: "POST",
  headers: {
    "X-API-Key": "${key}"
  },
  body: formData
});

const data = await response.json();
console.log(data);`;
  };

  return (
    <div className="dev-page">
      <div className="dev-container">
        {/* 1. Hero Section */}
        <header className="dev-hero fade-in">
          <div className="hero-content">
            <div className="hero-badge">Production Ready v1.1</div>
            <h1>Yemen LPR Developer API</h1>
            <p className="hero-subtitle">
              Integrate enterprise-grade vehicle recognition into your
              applications. Built for accuracy, speed, and reliability.
            </p>
            <div className="hero-actions">
              <button
                onClick={() =>
                  document
                    .getElementById("auth-section")
                    .scrollIntoView({ behavior: "smooth" })
                }
                className="btn btn-primary"
              >
                Get API Key
              </button>
              <button
                onClick={() =>
                  document
                    .getElementById("docs-section")
                    .scrollIntoView({ behavior: "smooth" })
                }
                className="btn btn-secondary"
              >
                View Documentation
              </button>
            </div>
          </div>
        </header>

        {/* 2. Who is this API for? */}
        <section className="dev-section fade-in-up">
          <h2 className="section-title">Built for Scale</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="icon-wrapper traffic">🚦</div>
              <h3>Traffic Systems</h3>
              <p>Automated violation detection and traffic flow monitoring.</p>
            </div>
            <div className="feature-card">
              <div className="icon-wrapper security">🛡️</div>
              <h3>Security & Access</h3>
              <p>Gate control verification and secure entry automation.</p>
            </div>
            <div className="feature-card">
              <div className="icon-wrapper city">🏙️</div>
              <h3>Smart Cities</h3>
              <p>Urban planning data and vehicle density analysis.</p>
            </div>
            <div className="feature-card">
              <div className="icon-wrapper research">🔬</div>
              <h3>Research</h3>
              <p>Advanced computer vision datasets and analysis.</p>
            </div>
          </div>
        </section>

        {/* 3. Authentication */}
        <section id="auth-section" className="dev-section fade-in-up">
          <div className="section-header">
            <h2 className="section-title">Authentication</h2>
            <p className="section-desc">
              Requests are authenticated using the <code>X-API-Key</code>{" "}
              header. Your API keys carry many privileges, so be sure to keep
              them secure.
            </p>
          </div>

          <div className="auth-card">
            <div className="auth-row">
              <div className="key-info">
                <span className="key-label">Server Key</span>
                <div className="key-value-wrapper">
                  <code className="key-value">
                    {apiKey ? apiKey : "No active key"}
                  </code>
                  {apiKey && (
                    <span className="status-badge active">Active</span>
                  )}
                </div>
              </div>
              <div className="key-actions">
                <button
                  className="btn btn-sm btn-outline"
                  onClick={createApiKey}
                  disabled={isGeneratingKey}
                >
                  {isGeneratingKey
                    ? "Generating..."
                    : apiKey
                      ? "Roll Key"
                      : "Create Key"}
                </button>
                {apiKey && (
                  <button
                    className="btn btn-sm btn-icon"
                    onClick={() => copyToClipboard(apiKey, "apikey")}
                  >
                    {copied.apikey ? "✓" : "📋"}
                  </button>
                )}
              </div>
            </div>
            <div className="code-snippet-simple">
              <span className="comment"># Authentication Header</span>
              <br />
              <span className="key">X-API-Key</span>:{" "}
              <span className="string">{apiKey || "YOUR_API_KEY"}</span>
            </div>
          </div>
        </section>

        {/* 4. API Endpoints */}
        <section id="docs-section" className="dev-section fade-in-up">
          <h2 className="section-title">API Reference</h2>

          <div className="api-tabs">
            <button
              className={`tab-btn ${activeTab === "image" ? "active" : ""}`}
              onClick={() => setActiveTab("image")}
            >
              Image API
            </button>
            <button
              className={`tab-btn ${activeTab === "video" ? "active" : ""}`}
              onClick={() => setActiveTab("video")}
            >
              Video API
            </button>
          </div>

          <div className="api-content-card">
            {/* Endpoint Header */}
            <div className="endpoint-header">
              <span className="method-badge post">POST</span>
              <span className="endpoint-path">
                /api/v1/predict/{activeTab}/
              </span>
            </div>

            <p className="endpoint-desc">
              {activeTab === "image"
                ? "Detects license plates and vehicle attributes in a single static image."
                : "Processes video files frame-by-frame to track and identify vehicles."}
            </p>

            <div className="split-view">
              {/* Left Column: Params */}
              <div className="col-left">
                <h4 className="col-title">Parameters</h4>
                <table className="docs-table">
                  <tbody>
                    <tr>
                      <td className="param-name">
                        file <span className="req">*</span>
                      </td>
                      <td className="param-type">binary</td>
                      <td className="param-desc">
                        {activeTab === "image"
                          ? "JPG, PNG, or WebP image."
                          : "MP4, AVI container."}{" "}
                        Max size: {activeTab === "image" ? "10MB" : "50MB"}.
                      </td>
                    </tr>
                    {activeTab === "image" && (
                      <tr>
                        <td className="param-name">overlay</td>
                        <td className="param-type">boolean</td>
                        <td className="param-desc">
                          Returns a URL to the annotated image. Default:{" "}
                          <code>true</code>.
                        </td>
                      </tr>
                    )}
                    {activeTab === "video" && (
                      <tr>
                        <td className="param-name">skip_frames</td>
                        <td className="param-type">integer</td>
                        <td className="param-desc">
                          Process every Nth frame. Default: <code>2</code>.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>

                <h4 className="col-title mt-4">Response Object</h4>
                <div className="code-block json-block">
                  <pre>
                    {activeTab === "image"
                      ? `{
  "success": true,
  "execution_time": 0.42,
  "results": [
    {
      "plate_number": "52489",
      "confidence": 0.98,
      "vehicle_type": "bus",
      "governorate": "Sanaa"
    }
  ],
  "overlay_url": "/media/overlay.jpg"
}`
                      : `{
  "success": true,
  "execution_time": 2.15,
  "frames_processed": 150,
  "unique_plates": ["52489", "10293"]
}`}
                  </pre>
                </div>
              </div>

              {/* Right Column: Code Examples */}
              <div className="col-right">
                <h4 className="col-title">Example Request</h4>

                <div className="code-tabs-inner">
                  <div className="code-label">cURL</div>
                  <div className="code-block dark">
                    <pre>{getCurlExample(activeTab)}</pre>
                    <button
                      className="copy-btn-corner"
                      onClick={() =>
                        copyToClipboard(getCurlExample(activeTab), "curl")
                      }
                    >
                      {copied.curl ? "Copied" : "Copy"}
                    </button>
                  </div>

                  <div className="code-label mt-3">JavaScript</div>
                  <div className="code-block dark">
                    <pre>{getJsExample(activeTab)}</pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 5. Error Handling */}
        <section className="dev-section fade-in-up">
          <h2 className="section-title">Errors</h2>
          <p className="section-desc">
            Standard HTTP status codes are used to communicate success or
            failure.
          </p>

          <table className="docs-table full-width">
            <thead>
              <tr>
                <th style={{ width: "20%" }}>Code</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <span className="status-code c400">400 Bad Request</span>
                </td>
                <td>
                  The request was unacceptable, often due to missing parameters
                  or invalid file format.
                </td>
              </tr>
              <tr>
                <td>
                  <span className="status-code c401">401 Unauthorized</span>
                </td>
                <td>
                  No valid API key provided. Check your <code>X-API-Key</code>{" "}
                  header.
                </td>
              </tr>
              <tr>
                <td>
                  <span className="status-code c429">
                    429 Too Many Requests
                  </span>
                </td>
                <td>
                  Too many requests hit the API too quickly. We recommend an
                  exponential backoff.
                </td>
              </tr>
              <tr>
                <td>
                  <span className="status-code c500">500 Server Error</span>
                </td>
                <td>Something went wrong on our end.</td>
              </tr>
            </tbody>
          </table>
        </section>

        {/* 6. AI Pipeline Visualization */}
        <section className="dev-section fade-in-up">
          <h2 className="section-title">AI Pipeline Architecture</h2>
          <p className="section-desc">
            Our multi-stage inference pipeline ensures maximum accuracy with
            optimized throughput.
          </p>

          <div className="pipeline-vis">
            <div className="pipeline-step">
              <div className="step-badge">01</div>
              <h4>Segmentation</h4>
              <p>YOLOv8-Seg</p>
              <span className="step-detail">Vehicle extraction</span>
            </div>
            <div className="pipeline-arrow">→</div>
            <div className="pipeline-step">
              <div className="step-badge">02</div>
              <h4>Detection</h4>
              <p>YOLOv8</p>
              <span className="step-detail">Plate localization</span>
            </div>
            <div className="pipeline-arrow">→</div>
            <div className="pipeline-step">
              <div className="step-badge">03</div>
              <h4>OCR</h4>
              <p>EasyOCR</p>
              <span className="step-detail">Character recognition</span>
            </div>
            <div className="pipeline-arrow">→</div>
            <div className="pipeline-step final">
              <div className="step-badge">04</div>
              <h4>Output</h4>
              <p>JSON / API</p>
              <span className="step-detail">Structured data</span>
            </div>
          </div>
        </section>

        {/* 7. Performance */}
        <section className="dev-section fade-in-up">
          <h2 className="section-title">Performance & Reliability</h2>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-val">99.9%</div>
              <div className="stat-label">Uptime</div>
            </div>
            <div className="stat-card">
              <div className="stat-val">&lt;400ms</div>
              <div className="stat-label">Latency (GPU)</div>
            </div>
            <div className="stat-card">
              <div className="stat-val">Auto</div>
              <div className="stat-label">GPU/CPU Scaling</div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Developers;
