import React from 'react';
import './MagicBento.css';

const MagicBento = ({ 
  children, 
  className = '', 
  variant = 'default',
  onClick,
  disabled = false,
  ...props 
}) => {
  const baseClasses = 'magic-bento';
  const variantClasses = {
    default: 'magic-bento-default',
    primary: 'magic-bento-primary',
    secondary: 'magic-bento-secondary',
    success: 'magic-bento-success',
    warning: 'magic-bento-warning',
    danger: 'magic-bento-danger'
  };

  const classes = [
    baseClasses,
    variantClasses[variant] || variantClasses.default,
    disabled ? 'magic-bento-disabled' : '',
    className
  ].filter(Boolean).join(' ');

  return (
    <div 
      className={classes}
      onClick={disabled ? undefined : onClick}
      {...props}
    >
      <div className="magic-bento-content">
        {children}
      </div>
      <div className="magic-bento-glow"></div>
    </div>
  );
};

export default MagicBento;

