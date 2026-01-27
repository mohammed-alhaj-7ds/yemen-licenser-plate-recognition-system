import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./AskAssistant.css";

// Context-Aware Knowledge Base
const KNOWLEDGE_BASE = {
  // Global & Home Context
  general: [
    { id: "accuracy", label: "How accurate is the system?" },
    { id: "try_demo", label: "Try a live demo" },
    { id: "models", label: "What AI models are used?" },
  ],
  // Developers Context
  developers: [
    { id: "api_key", label: "How do I get an API Key?" },
    { id: "rate_limits", label: "What are the rate limits?" },
    { id: "sdk", label: "Do you have an SDK?" },
    { id: "errors", label: "Common error codes?" },
  ],
  // Use Cases Context
  use_cases: [
    { id: "smart_cities", label: "Usage in Smart Cities?" },
    { id: "real_time", label: "Is it real-time?" },
    { id: "security", label: "Security applications?" },
  ],

  // Professional Responses
  answers: {
    accuracy: {
      title: "System Accuracy",
      text: "The system achieves **96%+ accuracy** on standard Yemeni license plates under varying lighting conditions. It uses a specialized YOLOv8 detection model trained on a localized dataset.",
      cta: { text: "View Performance Stats", link: "/developers" },
    },
    try_demo: {
      title: "Live Demo",
      text: "You can test the system directly in your browser. Upload an image to see the detection pipeline in action.",
      cta: { text: "Start Demo", link: "/#demo" }, // Assuming homepage has a demo section
    },
    models: {
      title: "AI Architecture",
      text: "We use a multi-stage pipeline: **YOLOv8-Seg** for vehicle extraction, followed by a dedicated **YOLOv8** plate detector, and **EasyOCR** for text recognition. This ensures high precision.",
      cta: { text: "See Pipeline", link: "/developers" },
    },
    api_key: {
      title: "Authentication",
      text: "Access to the API requires an API Key. You can generate one instantly in the Developers dashboard. Include it in the `X-API-Key` header.",
      cta: { text: "Generate Key", link: "/developers" },
    },
    rate_limits: {
      title: "API Limits",
      text: "Standard keys differ by tier. The free tier allows **100 requests/hour**. For higher throughput, please contact sales or enterprise support.",
      cta: null,
    },
    sdk: {
      title: "SDK Support",
      text: "Currently, we provide RESTful endpoints compatible with any language (Python, JS, Go). Official SDKs are on our roadmap for Q4.",
      cta: { text: "View Examples", link: "/developers" },
    },
    errors: {
      title: "Error Handling",
      text: "We use standard HTTP codes: `400` for bad input, `401` for auth issues, and `429` for rate limits. The body contains a detailed JSON error message.",
      cta: null,
    },
    smart_cities: {
      title: "Smart City Integration",
      text: "Yemen LPR integrates with urban infrastructure to monitor traffic flow, detect congestion, and provide data for automated tolling systems.",
      cta: { text: "Read Use Case", link: "/use-cases" },
    },
    real_time: {
      title: "Real-Time Processing",
      text: "Yes. With GPU acceleration (CUDA), the system processes video feeds with latency under **100ms per frame**, making it suitable for live monitoring.",
      cta: null,
    },
    security: {
      title: "Security & Access",
      text: "The system automates gate access control by verifying license plates against an allowlist in real-time, enhancing facility security.",
      cta: { text: "Security Details", link: "/use-cases" },
    },
    default: {
      title: "Support Scope",
      text: "I can help only with the Yemen LPR platform, its APIs, and integration details. Please simply ask about the system.",
      cta: null,
    },
  },
};

const AskAssistant = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [currentChips, setCurrentChips] = useState([]);

  const location = useLocation();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  // Initialize Greeting based on time
  useEffect(() => {
    const hour = new Date().getHours();
    const greeting =
      hour < 12
        ? "Good morning"
        : hour < 18
          ? "Good afternoon"
          : "Good evening";

    setMessages([
      {
        type: "bot",
        content: {
          title: `${greeting} 👋`,
          text: "I am the **LPR AI Assistant**. Ask me about the API, models, or integration.",
        },
      },
    ]);
  }, []);

  // Update Context Chips based on Route
  useEffect(() => {
    const path = location.pathname;
    if (path.includes("developers")) {
      setCurrentChips(KNOWLEDGE_BASE.developers);
    } else if (path.includes("use-cases")) {
      setCurrentChips(KNOWLEDGE_BASE.use_cases);
    } else {
      setCurrentChips(KNOWLEDGE_BASE.general);
    }
  }, [location]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, isOpen]);

  const handleChipClick = (key, label) => {
    setMessages((prev) => [
      ...prev,
      { type: "user", content: { text: label } },
    ]);
    setIsTyping(true);

    // Simulate AI "Thinking" time
    setTimeout(() => {
      const response =
        KNOWLEDGE_BASE.answers[key] || KNOWLEDGE_BASE.answers.default;
      setMessages((prev) => [...prev, { type: "bot", content: response }]);
      setIsTyping(false);
    }, 800);
  };

  const handleCtaClick = (link) => {
    if (link.startsWith("/")) {
      navigate(link);
      // Optional: Close panel on navigation if needed
      // setIsOpen(false);
    } else {
      window.open(link, "_blank");
    }
  };

  const toggleOpen = () => setIsOpen(!isOpen);

  // Helper to parse simple markdown (bold)
  const renderText = (text) => {
    if (!text) return null;
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return part;
    });
  };

  return (
    <>
      <button
        className={`ask-fab ${isOpen ? "active" : ""} fade-in-up delay-5`}
        onClick={toggleOpen}
        aria-label="Ask AI Assistant"
      >
        <span className="fab-icon">✨</span>
        <span className="fab-text">Ask AI</span>
      </button>

      <div className={`assistant-panel ${isOpen ? "open" : ""}`}>
        <div className="assistant-header">
          <div className="header-info">
            <h3>LPR Assistant</h3>
            <span className="status-indicator"></span>
          </div>
          <button className="close-btn" onClick={toggleOpen}>
            ✕
          </button>
        </div>

        <div className="assistant-body">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.type} slide-in`}>
              {msg.type === "bot" && <div className="avatar">🤖</div>}
              <div className="bubble">
                {msg.content.title && (
                  <div className="msg-title">{msg.content.title}</div>
                )}
                <div className="msg-text">{renderText(msg.content.text)}</div>

                {msg.content.cta && (
                  <button
                    className="msg-cta"
                    onClick={() => handleCtaClick(msg.content.cta.link)}
                  >
                    {msg.content.cta.text} →
                  </button>
                )}
              </div>
            </div>
          ))}

          {isTyping && (
            <div className="message bot">
              <div className="avatar">🤖</div>
              <div className="bubble typing">
                <span className="typing-text">Analyzing</span>
                <span className="dot">.</span>
                <span className="dot">.</span>
                <span className="dot">.</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="assistant-footer">
          <div className="chips-container">
            {currentChips.map((chip) => (
              <button
                key={chip.id}
                className="chip"
                onClick={() => handleChipClick(chip.id, chip.label)}
                disabled={isTyping}
              >
                {chip.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div
        className={`assistant-backdrop ${isOpen ? "active" : ""}`}
        onClick={toggleOpen}
      />
    </>
  );
};

export default AskAssistant;
