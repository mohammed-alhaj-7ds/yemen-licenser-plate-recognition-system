import { Link } from 'react-router-dom';
import './NotFound.css';

function NotFound() {
  return (
    <div className="notfound-page">
      <div className="notfound-content">
        <div className="notfound-code">404</div>
        <h1 className="notfound-title">الصفحة غير موجودة</h1>
        <p className="notfound-desc">
          عذراً، الصفحة التي تبحث عنها غير موجودة أو تم نقلها.
        </p>
        <Link to="/" className="notfound-btn">
          🏠 العودة للرئيسية
        </Link>
      </div>
    </div>
  );
}

export default NotFound;
