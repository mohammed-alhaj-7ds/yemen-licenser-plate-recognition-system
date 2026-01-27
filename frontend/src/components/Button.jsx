import './Button.css';

function Button({
  children,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  loadingText = 'جاري المعالجة…',
  onClick,
  type = 'button',
  icon,
  fullWidth = false,
  ...props
}) {
  const className = [
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    disabled && 'btn-disabled',
    loading && 'btn-loading',
    fullWidth && 'btn-full-width',
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <button
      className={className}
      disabled={disabled || loading}
      onClick={onClick}
      type={type}
      aria-disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <>
          <span className="btn-spinner"></span>
          <span>{loadingText}</span>
        </>
      ) : (
        <>
          {icon && <span className="btn-icon">{icon}</span>}
          {children}
        </>
      )}
    </button>
  );
}

export default Button;
