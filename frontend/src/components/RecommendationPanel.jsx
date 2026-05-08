import React from 'react';
import BenchmarkBar from './BenchmarkBar';

const RecommendationPanel = ({ recommendations = [], detectedCategory, weightsUsed = {} }) => {
  if (!recommendations.length) return null;

  return (
    <div className="w-full mt-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="font-display text-2xl font-bold text-text">Top Recommendations</h2>
        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary/10 text-primary border border-primary/20">
          Detected: {detectedCategory}
        </span>
      </div>
      
      <div className="space-y-6 animate-stagger">
        {recommendations.map((rec) => (
          <div 
            key={rec.model_id} 
            className="recommendation-item bg-surface border border-border rounded-lg p-5 sm:p-6 shadow-sm hover:border-violet transition-colors duration-300"
          >
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 mb-4">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-surface-2 border border-divider flex items-center justify-center font-display font-bold text-text shadow-inner">
                  #{rec.rank}
                </div>
                <div>
                  <h3 className="font-display text-xl font-bold text-text flex items-center gap-2">
                    {rec.model_name}
                  </h3>
                  <span className="inline-block mt-1 text-xs font-medium text-violet px-2 py-0.5 rounded bg-surface-2 border border-divider">
                    {rec.provider || 'Unknown'}
                  </span>
                </div>
              </div>
              <div className="flex flex-col items-start sm:items-end">
                <div className="text-sm text-text-muted mb-1">Final Match Score</div>
                <div className="font-mono text-2xl font-bold text-success drop-shadow-sm">
                  {(rec.final_score * 100).toFixed(1)}%
                </div>
              </div>
            </div>
            
            <div className="mt-6 border-t border-divider pt-4">
              <h4 className="text-xs uppercase tracking-wider text-text-faint mb-3 font-semibold">
                Key Metrics for {detectedCategory}
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2">
                {Object.keys(weightsUsed).map((benchName, idx) => {
                  const breakdown = rec.score_breakdown[benchName];
                  const rawScore = breakdown ? breakdown.raw : 0;
                  const isElo = benchName.toLowerCase().includes('elo');
                  const maxScore = isElo ? 1300 : 100;
                  
                  // Alternate colors
                  const colors = ["bg-primary", "bg-violet", "bg-amber", "bg-success"];
                  const color = colors[idx % colors.length];

                  return (
                    <BenchmarkBar
                      key={benchName}
                      modelName={rec.model_name}
                      benchmark={benchName}
                      score={rawScore}
                      maxScore={maxScore}
                      color={color}
                    />
                  );
                })}
              </div>
            </div>
            
            {rec.reasoning && (
              <div className="mt-5 bg-surface-2 rounded-md p-3 border border-divider border-l-4 border-l-amber">
                <p className="text-sm italic text-text-muted">
                  "{rec.reasoning}"
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecommendationPanel;
