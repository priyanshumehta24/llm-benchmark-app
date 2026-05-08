import React from 'react';
import BenchmarkBar from './BenchmarkBar';

const ModelCard = ({ model }) => {
  const { id, name, provider, family, is_open_source, scores = [] } = model;
  
  // Get up to top 3 scores to display on the card
  const topScores = scores.slice(0, 3);

  return (
    <div className="model-card bg-surface border border-border rounded-lg p-5 transition-colors duration-200 hover:border-primary overflow-hidden flex flex-col h-full shadow-sm hover:shadow-primary/10">
      <div className="flex justify-between items-start mb-4">
        <div className="mr-3 overflow-hidden">
          <h3 className="font-display text-lg font-bold text-text truncate" title={name}>
            {name}
          </h3>
          <div className="text-sm text-text-muted mt-1 truncate" title={family || 'Unknown'}>
            {family || 'Unknown Family'}
          </div>
        </div>
        <div className="flex flex-col items-end gap-2 flex-shrink-0">
          {provider && (
            <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-surface-2 text-violet border border-divider">
              {provider}
            </span>
          )}
          <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${
            is_open_source 
              ? 'bg-success/10 text-success border-success/20' 
              : 'bg-amber/10 text-amber border-amber/20'
          }`}>
            {is_open_source ? 'Open Source' : 'Proprietary'}
          </span>
        </div>
      </div>
      
      <div className="mt-auto pt-4 border-t border-divider">
        <h4 className="text-xs uppercase tracking-wider text-text-faint mb-3 font-semibold">
          Top Benchmarks
        </h4>
        {topScores.length > 0 ? (
          <div className="space-y-1">
            {topScores.map((scoreObj, idx) => {
              // Determine if score is Elo (approx 1000-1300 scale) or percent (0-100)
              const isElo = scoreObj.score_type === 'elo' || 
                           (scoreObj.benchmark_name && scoreObj.benchmark_name.toLowerCase().includes('elo'));
              const maxScore = isElo ? 1300 : 100; 
              
              // Map colors sequentially based on index
              const color = idx === 0 ? "bg-primary" : idx === 1 ? "bg-violet" : "bg-text-muted";

              return (
                <BenchmarkBar
                  key={idx}
                  modelName={name}
                  benchmark={scoreObj.benchmark_name}
                  score={scoreObj.score}
                  maxScore={maxScore}
                  color={color}
                />
              );
            })}
          </div>
        ) : (
          <div className="text-sm text-text-faint italic py-2">
            No benchmark data available
          </div>
        )}
      </div>
    </div>
  );
};

export default ModelCard;
