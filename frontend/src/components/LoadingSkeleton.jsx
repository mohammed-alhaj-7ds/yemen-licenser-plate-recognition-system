import "./LoadingSkeleton.css";

function LoadingSkeleton() {
  return (
    <div className="loading-skeleton">
      <div className="skeleton-header">
        <div className="skeleton-title"></div>
        <div className="skeleton-subtitle"></div>
      </div>

      <div className="skeleton-cards">
        <div className="skeleton-card">
          <div className="skeleton-card-header"></div>
          <div className="skeleton-card-body">
            <div className="skeleton-line"></div>
            <div className="skeleton-line"></div>
            <div className="skeleton-line short"></div>
          </div>
        </div>

        <div className="skeleton-card">
          <div className="skeleton-card-header"></div>
          <div className="skeleton-card-body">
            <div className="skeleton-line"></div>
            <div className="skeleton-line"></div>
            <div className="skeleton-line short"></div>
          </div>
        </div>
      </div>

      <div className="skeleton-image"></div>
    </div>
  );
}

export default LoadingSkeleton;
