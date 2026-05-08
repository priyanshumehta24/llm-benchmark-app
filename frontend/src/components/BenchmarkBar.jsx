import React, { useEffect, useRef } from 'react';
import anime from 'animejs';

const BenchmarkBar = ({ modelName, benchmark, score, maxScore = 100, color = 'bg-primary' }) => {
  // Ensure percentage is between 0 and 100 for the visual bar
  const percentage = Math.min(Math.max((score / maxScore) * 100, 0), 100);
  const fillRef = useRef(null);

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      if (fillRef.current) fillRef.current.style.width = `${percentage}%`;
      return;
    }

    if (fillRef.current) {
      anime({
        targets: fillRef.current,
        width: ['0%', `${percentage}%`],
        duration: 600,
        easing: 'easeOutExpo'
      });
    }
  }, [percentage]);

  
  // Format display score. If it's a percentage scale (<= 100), add %.
  const displayScore = maxScore <= 100 
    ? `${Number(score).toFixed(1)}%` 
    : Number(score).toFixed(0);

  return (
    <div className="w-full mb-3">
      <div className="flex justify-between items-end mb-1">
        <span className="text-sm font-medium text-text-muted truncate mr-2" title={benchmark}>
          {benchmark}
        </span>
        <span className="text-sm font-mono text-text flex-shrink-0">
          {displayScore}
        </span>
      </div>
      <div className="w-full bg-surface-offset rounded-full h-2 overflow-hidden">
        <div 
          ref={fillRef}
          className={`benchmark-bar-fill h-full rounded-full ${color}`}
          style={{ width: '0%' }}
        ></div>
      </div>
    </div>
  );
};

export default BenchmarkBar;
