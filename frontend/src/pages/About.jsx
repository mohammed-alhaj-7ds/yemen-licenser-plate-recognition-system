import { Link } from "react-router-dom";
import "./About.css";

function About() {
  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="about-hero-content">
          <h1 className="about-title">
            <span className="about-icon">🚗</span>
            About Yemen LPR
          </h1>
          <p className="about-tagline">
            Bridging the gap between academic research and commercial-grade
            vehicle recognition infrastructure in Yemen.
          </p>
        </div>
      </section>

      <section className="about-content">
        <div className="about-container">
          {/* Mission */}
          <div className="about-card about-card-highlight">
            <h2 className="about-heading">
              <span className="about-heading-icon">🎯</span>
              Our Mission
            </h2>
            <p className="about-text">
              To develop a robust, localized computer vision solution capable of
              detecting and recognizing Yemeni license plates with high
              accuracy, addressing specific challenges like diverse plate
              formats and varying environmental conditions.
            </p>
          </div>

          {/* Problem Statement (Academic Requirement) */}
          <div className="about-card">
            <h2 className="about-heading">
              <span className="about-heading-icon">⚠️</span>
              The Problem
            </h2>
            <p className="about-text mb-2">
              Traditional OCR systems fail on Yemeni plates due to unique
              layouts and mixed Arabic/English text.
            </p>
            <ul className="about-list">
              <li>
                <strong>Complex Backgrounds</strong>: Urban clutter and dust
                affecting visibility.
              </li>
              <li>
                <strong>Plate Variations</strong>: Private, commercial,
                government, and army plates.
              </li>
              <li>
                <strong>Manual Logging</strong>: Inefficiency and errors in
                manual checkpoints.
              </li>
            </ul>
          </div>

          {/* Solution Architecture (Academic Requirement) */}
          <div className="about-card">
            <h2 className="about-heading">
              <span className="about-heading-icon">⚡</span>
              Solution Architecture
            </h2>
            <p className="about-text mb-4">
              A multi-stage deep learning pipeline optimized for accuracy and
              throughput:
            </p>
            <div className="pipeline-visual">
              <div className="p-step">Input Image</div>
              <div className="p-arrow">→</div>
              <div className="p-step">
                YOLOv8-Seg <small>(Vehicle Extraction)</small>
              </div>
              <div className="p-arrow">→</div>
              <div className="p-step">
                YOLOv8 <small>(Plate Detection)</small>
              </div>
              <div className="p-arrow">→</div>
              <div className="p-step">
                EasyOCR <small>(Text Recognition)</small>
              </div>
              <div className="p-arrow">→</div>
              <div className="p-step">
                Post-Processing <small>(Governorate Logic)</small>
              </div>
            </div>
          </div>

          {/* Tech Stack */}
          <div className="about-card">
            <h2 className="about-heading">
              <span className="about-heading-icon">🛠️</span>
              Technology Stack
            </h2>
            <div className="tech-grid">
              <div className="tech-item">
                <div className="tech-icon">🐍</div>
<<<<<<< HEAD
                <h3>Python & Deep Learning</h3>
=======
                <h3>Python & Deep Learning & Computer vision</h3>
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
                <p>PyTorch, Ultralytics YOLOv8, OpenCV, NumPy</p>
              </div>
              <div className="tech-item">
                <div className="tech-icon">🌐</div>
                <h3>Backend API</h3>
                <p>Django REST Framework, Swagger/OpenAPI</p>
              </div>
              <div className="tech-item">
                <div className="tech-icon">⚛️</div>
                <h3>Frontend</h3>
                <p>React, Vite, CSS Modules, Modern Hooks</p>
              </div>
              <div className="tech-item">
                <div className="tech-icon">🐳</div>
                <h3>Deployment</h3>
                <p>Docker, Gunicorn, Nginx Ready</p>
              </div>
            </div>
          </div>

          {/* Team Section (University Requirement) */}
          <div className="about-card">
            <h2 className="about-heading">
              <span className="about-heading-icon">👥</span>
              The Team
            </h2>
            <p className="about-text text-center mb-4">
              Developed as a capstone project for the Computer Vision course.
            </p>
            <div className="team-grid">
              <div className="team-member highlight">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Mohamed Mohamed Yahya Al-Hajj</div>
<<<<<<< HEAD
                <div className="team-role">Team Lead & Full Stack</div>
=======
                <div className="team-role">
                  Team Lead & Full Stack & ML Engineer
                </div>
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
              </div>
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Manaf Fahmi Al-Banna</div>
                <div className="team-role">ML Engineer</div>
              </div>
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Mohammed Yousef Al-Rubai</div>
                <div className="team-role">ML Engineer</div>
              </div>
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Muhannad Al-Ameri</div>
                <div className="team-role">ML Engineer</div>
              </div>
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Marwan Bawzir</div>
                <div className="team-role">ML Engineer</div>
              </div>
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Ali Al-Nusairi</div>
                <div className="team-role">ML Engineer</div>
              </div>
<<<<<<< HEAD
=======
              <div className="team-member">
                <div className="team-avatar">👨‍💻</div>
                <div className="team-name">Al-Ezz Al-Mahjary</div>
                <div className="team-role">
                  Team Lead & Full Stack & ML Engineer
                </div>
              </div>
>>>>>>> 1ac0cac23aeaa4d1df9946be393595cfb8b764f9
            </div>
          </div>

          {/* Actions */}
          <div className="about-actions">
            <Link to="/" className="about-btn about-btn-primary">
              View Demo
            </Link>
            <Link to="/developers" className="about-btn about-btn-secondary">
              API Documentation
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;
