import React, { useState } from 'react';
import UseCaseSelector from '../components/UseCaseSelector';
import RecommendationPanel from '../components/RecommendationPanel';
import client from '../api/client';

const Recommend = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleRecommend = async (text) => {
    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await client.post('/api/recommend', {
        use_case_text: text,
        top_n: 5
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'An error occurred while fetching recommendations. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="mb-8 text-center">
        <h1 className="font-display text-3xl md:text-4xl font-bold text-text mb-4">
          Model Recommender
        </h1>
        <p className="text-text-muted text-lg max-w-2xl mx-auto">
          Describe what you want to build or do, and we'll recommend the best models based on actual benchmark data.
        </p>
      </div>

      <UseCaseSelector onSubmit={handleRecommend} isLoading={isLoading} />

      {error && (
        <div className="mt-6 bg-error/10 border border-error/20 rounded-md p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-error" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-error">Recommendation Failed</h3>
              <div className="mt-2 text-sm text-error/90">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {isLoading && (
        <div className="mt-8 space-y-6">
          {Array.from({ length: 3 }).map((_, idx) => (
            <div key={idx} className="bg-surface border border-border rounded-lg p-6 animate-pulse">
              <div className="flex items-start gap-4 mb-4">
                <div className="w-10 h-10 rounded-full bg-surface-2 flex-shrink-0"></div>
                <div className="flex-1">
                  <div className="h-6 bg-surface-2 rounded w-1/4 mb-2"></div>
                  <div className="h-4 bg-surface-2 rounded w-1/6"></div>
                </div>
                <div className="w-20 h-8 bg-surface-2 rounded"></div>
              </div>
              <div className="mt-6 border-t border-divider pt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="h-6 bg-surface-2 rounded w-full"></div>
                <div className="h-6 bg-surface-2 rounded w-full"></div>
                <div className="h-6 bg-surface-2 rounded w-full"></div>
              </div>
              <div className="mt-5 h-10 bg-surface-2 rounded w-full"></div>
            </div>
          ))}
        </div>
      )}

      {result && !isLoading && (
        <RecommendationPanel 
          recommendations={result.recommendations} 
          detectedCategory={result.detected_category} 
          weightsUsed={result.weights_used} 
        />
      )}
    </div>
  );
};

export default Recommend;
