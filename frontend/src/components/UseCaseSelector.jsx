import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const UseCaseSelector = ({ onSubmit, isLoading }) => {
  const [text, setText] = useState('');

  const { data: categories, isLoading: isLoadingCategories } = useQuery({
    queryKey: ['usecases'],
    queryFn: async () => {
      const response = await client.get('/api/usecases');
      return response.data;
    }
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text);
    }
  };

  return (
    <div className="w-full bg-surface border border-border rounded-lg p-6 shadow-sm">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="usecase-input" className="block text-sm font-medium text-text-muted mb-2">
            Describe your task
          </label>
          <textarea
            id="usecase-input"
            rows="3"
            className="w-full bg-bg border border-divider rounded-md px-4 py-3 text-text placeholder-text-faint focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-shadow resize-none"
            placeholder="Describe your use case... e.g. I need a model for legal document analysis"
            value={text}
            onChange={(e) => setText(e.target.value)}
          ></textarea>
        </div>
        
        <div className="mb-6">
          <span className="block text-xs font-medium text-text-faint uppercase tracking-wider mb-2">
            Or select a common category
          </span>
          <div className="flex flex-wrap gap-2">
            {isLoadingCategories ? (
              <span className="text-sm text-text-muted">Loading categories...</span>
            ) : categories && categories.length > 0 ? (
              categories.map(cat => (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setText(cat.label)}
                  className="px-3 py-1.5 rounded-full text-xs font-medium bg-surface-2 text-text-muted border border-divider hover:border-primary hover:text-text transition-colors"
                >
                  {cat.label}
                </button>
              ))
            ) : null}
          </div>
        </div>
        
        <button
          type="submit"
          disabled={isLoading || !text.trim()}
          className="w-full flex justify-center items-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-bg bg-primary hover:bg-primary-hover focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-surface focus:ring-primary transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-bold tracking-wide"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-bg" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing...
            </>
          ) : (
            'Find Best Model \u2192'
          )}
        </button>
      </form>
    </div>
  );
};

export default UseCaseSelector;
