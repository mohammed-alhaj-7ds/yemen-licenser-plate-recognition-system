import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-title">🚗 Yemen LPR</h3>
            <p className="footer-description">
              نظام ذكي للتعرف على لوحات السيارات اليمنية باستخدام تقنيات التعلم العميق
            </p>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">التقنيات</h4>
            <p className="footer-tech">
              Powered by <strong>YOLOv8</strong> + <strong>EasyOCR</strong>
            </p>
            <p className="footer-tech">
              Built with <strong>Django</strong> + <strong>React</strong>
            </p>
          </div>

          <div className="footer-section">
            <h4 className="footer-heading">روابط سريعة</h4>
            <div className="footer-links">
              <Link to="/" className="footer-link">الرئيسية</Link>
              <Link to="/developers" className="footer-link">للمطورين</Link>
              <Link to="/about" className="footer-link">حول المشروع</Link>
              <a href="/api/v1/docs/" className="footer-link" target="_blank" rel="noopener noreferrer">
                وثائق API
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            © 2026 Yemen License Plate Recognition System
            <br />
            <span className="footer-subtitle">مشروع جامعي في الرؤية الحاسوبية</span>
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
