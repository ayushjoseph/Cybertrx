import React from 'react';
import './BlurText.css';

const BlurText = ({ children, className = '', delay = 0 }) => {
  return (
    <span 
      className={`blur-text ${className}`}
      style={{ animationDelay: `${delay}ms` }}
    >
      {children}
    </span>
  );
};

export default BlurText;
