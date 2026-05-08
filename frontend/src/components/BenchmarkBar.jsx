import React from 'react';

const BenchmarkBar = ({ modelName, benchmark, score, maxScore = 100, color = 'bg-primary' }) => {
  // Ensure percentage is between 0 and 100 for the visual bar
  const percentage = Math.min(Math.max((score / maxScore) * 100, 0), 100);
  
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
          className={`benchmark-bar-fill h-full rounded-full ${color}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

export default BenchmarkBar;
