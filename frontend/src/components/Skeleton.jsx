import './Skeleton.css';

function Skeleton({ width, height, borderRadius = '8px' }) {
  return (
    <div
      className="skeleton"
      style={{
        width: width || '100%',
        height: height || '1rem',
        borderRadius,
      }}
    />
  );
}

export default Skeleton;
