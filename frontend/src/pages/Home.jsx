import React from 'react';
import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';
import ModelCard from '../components/ModelCard';

const Home = () => {
  // Fetch live stats
  const { data: statsData, isLoading: isLoadingStats } = useQuery({
    queryKey: ['lastUpdated'],
    queryFn: async () => {
      const response = await client.get('/api/last-updated');
      return response.data;
    }
  });

  // Fetch top models grid
  const { data: modelsData, isLoading: isLoadingModels } = useQuery({
    queryKey: ['models'],
    queryFn: async () => {
      const response = await client.get('/api/models');
      return response.data;
    }
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Section 1: Hero */}
      <section className="text-center mb-16 animate-fade-up">
        <h1 className="hero-heading font-display text-4xl md:text-5xl lg:text-6xl font-bold text-text mb-6">
          Find the Right LLM for Your <span className="text-primary">Use Case</span>
        </h1>
        <p className="text-xl text-text-muted mb-10 max-w-2xl mx-auto">
          Powered by public benchmarks. Updated daily.
        </p>
        <div className="hero-buttons flex flex-col sm:flex-row justify-center gap-4">
          <Link 
            to="/recommend" 
            className="inline-flex justify-center items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-bg bg-primary hover:bg-primary-hover transition-colors"
          >
            Get Recommendation &rarr;
          </Link>
          <Link 
            to="/compare" 
            className="inline-flex justify-center items-center px-6 py-3 border border-border text-base font-medium rounded-md text-text bg-surface-2 hover:bg-surface-offset transition-colors"
          >
            Compare Models
          </Link>
        </div>
      </section>

      {/* Section 2: Live Stats Bar */}
      <section className="bg-surface border border-border rounded-lg p-6 mb-16 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center divide-y md:divide-y-0 md:divide-x divide-divider">
          <div className="pt-4 md:pt-0">
            <div className="text-sm font-medium text-text-faint uppercase tracking-wider mb-1">Total Models</div>
            <div className="stat-number text-4xl font-bold font-mono text-primary">
              {isLoadingStats ? '-' : statsData?.models_count || 0}
            </div>
          </div>
          <div className="pt-4 md:pt-0">
            <div className="text-sm font-medium text-text-faint uppercase tracking-wider mb-1">Total Benchmarks</div>
            <div className="stat-number text-4xl font-bold font-mono text-violet">
              {isLoadingStats ? '-' : statsData?.scores_count || 0}
            </div>
          </div>
          <div className="pt-4 md:pt-0">
            <div className="text-sm font-medium text-text-faint uppercase tracking-wider mb-1">Last Updated</div>
            <div className="text-lg font-medium text-text mt-2">
              {isLoadingStats 
                ? 'Loading...' 
                : statsData?.last_updated 
                  ? new Date(statsData.last_updated).toLocaleDateString() 
                  : 'N/A'}
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Top Models Grid */}
      <section>
        <div className="flex justify-between items-end mb-8">
          <h2 className="text-2xl font-display font-bold text-text">Top Models</h2>
          <Link to="/compare" className="text-sm text-primary hover:text-primary-hover transition-colors">
            View all models &rarr;
          </Link>
        </div>
        
        <div className="models-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-stagger">
          {isLoadingModels ? (
            // Skeleton loaders
            Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="bg-surface border border-border rounded-lg p-5 h-[260px] animate-pulse flex flex-col">
                <div className="flex justify-between mb-4">
                  <div className="h-6 bg-surface-2 rounded w-1/2"></div>
                  <div className="h-5 bg-surface-2 rounded w-1/4"></div>
                </div>
                <div className="mt-auto space-y-4">
                  <div className="h-3 bg-surface-2 rounded w-full"></div>
                  <div className="h-3 bg-surface-2 rounded w-5/6"></div>
                  <div className="h-3 bg-surface-2 rounded w-4/6"></div>
                </div>
              </div>
            ))
          ) : modelsData && modelsData.length > 0 ? (
            modelsData.map(model => (
              <ModelCard key={model.id} model={model} />
            ))
          ) : (
            <div className="col-span-full text-center py-12 text-text-muted">
              No models found. Please ensure the backend is running and seeded.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;
