import React, { useEffect } from "react";
import "./UseCases.css";

const UseCases = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div className="use-cases-page">
      <div className="use-cases-container">
        {/* Hero Section */}
        <header className="uc-hero fade-in-down">
          <div className="uc-hero-content">
            <div className="uc-badge">Real-World Applications</div>
            <h1>Empowering Modern Infrastructure</h1>
            <p className="uc-subtitle">
              From smart cities to secure facilities, our AI-powered recognition
              system delivers actionable data where it matters most.
            </p>
          </div>
        </header>

        {/* Use Cases Grid */}
        <section className="uc-grid">
          {/* Card 1: Traffic */}
          <div className="uc-card delay-1 fade-in-up">
            <div className="uc-icon-wrapper traffic">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-traffic-cone"
              >
                <path d="M9.3 6.2a4.55 4.55 0 0 0 5.4 0" />
                <path d="M7.9 10.7c.9.8 2.4 1.3 4.1 1.3s3.2-.5 4.1-1.3" />
                <path d="M13.9 3.5a1.93 1.93 0 0 0-3.8-.1l-3 10c-.1.2-.1.4-.1.6 0 1.7 2.2 3 5 3s5-1.3 5-3c0-.2 0-.4-.1-.6l-3-10Z" />
              </svg>
            </div>
            <h3>Traffic Management</h3>
            <p>
              Automated vehicle identification for traffic monitoring,
              analytics, and enforcement systems. Detect violations and analyze
              flow patterns in real-time.
            </p>
          </div>

          {/* Card 2: Security */}
          <div className="uc-card delay-2 fade-in-up">
            <div className="uc-icon-wrapper security">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-shield-check"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10" />
                <path d="m9 12 2 2 4-4" />
              </svg>
            </div>
            <h3>Security & Access Control</h3>
            <p>
              Smart gate access and vehicle authorization for private and
              government facilities. Seamlessly grant entry to authorized
              personnel while flagging unknowns.
            </p>
          </div>

          {/* Card 3: Smart Cities */}
          <div className="uc-card delay-3 fade-in-up">
            <div className="uc-icon-wrapper city">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-building-2"
              >
                <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z" />
                <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" />
                <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2" />
                <path d="M10 6h4" />
                <path d="M10 10h4" />
                <path d="M10 14h4" />
                <path d="M10 18h4" />
              </svg>
            </div>
            <h3>Smart Cities</h3>
            <p>
              Vehicle flow data to support urban planning and intelligent
              transportation systems. Make data-driven decisions to reduce
              congestion and improve city living.
            </p>
          </div>

          {/* Card 4: Research */}
          <div className="uc-card delay-4 fade-in-up">
            <div className="uc-icon-wrapper research">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-microscope"
              >
                <path d="M6 18h8" />
                <path d="M3 22h18" />
                <path d="M14 22a7 7 0 1 0 0-14h-1" />
                <path d="M9 14h2" />
                <path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z" />
                <path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3" />
              </svg>
            </div>
            <h3>Research & Innovation</h3>
            <p>
              A real-world computer vision pipeline for AI research and local
              datasets. Contributing to the advancement of localized recognition
              models.
            </p>
          </div>
        </section>
      </div>
    </div>
  );
};

export default UseCases;
