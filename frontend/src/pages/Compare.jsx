import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import anime from 'animejs';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import client from '../api/client';
import RadarChart from '../components/RadarChart';

const Compare = () => {
  const [selectedModels, setSelectedModels] = useState([]);
  const [compareData, setCompareData] = useState(null);
  const [isComparing, setIsComparing] = useState(false);
  const [error, setError] = useState('');

  // Fetch available models
  const { data: models, isLoading: isLoadingModels } = useQuery({
    queryKey: ['models'],
    queryFn: async () => {
      const response = await client.get('/api/models');
      return response.data;
    }
  });

  const handleSelectModel = (e) => {
    const modelId = parseInt(e.target.value);
    if (!modelId) return;
    
    if (selectedModels.length >= 4) {
      setError('You can compare a maximum of 4 models at a time.');
      return;
    }
    
    if (selectedModels.some(m => m.id === modelId)) {
      return; // Already selected
    }
    
    const model = models.find(m => m.id === modelId);
    if (model) {
      setSelectedModels([...selectedModels, model]);
      setError('');
      // Reset Select value to empty
      e.target.value = "";
    }
  };

  const handleRemoveModel = (idToRemove) => {
    setSelectedModels(selectedModels.filter(m => m.id !== idToRemove));
    setCompareData(null); // Clear comparison when models change
  };

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (compareData && !isComparing) {
      anime.set('.compare-charts', { opacity: 0 });
      anime({
        targets: '.compare-charts',
        opacity: [0, 1],
        duration: 800,
        easing: 'easeOutExpo'
      });
    }
  }, [compareData, isComparing]);

  const handleCompare = async () => {
    if (selectedModels.length < 2) return;
    
    setIsComparing(true);
    setError('');
    
    try {
      const ids = selectedModels.map(m => m.id).join(',');
      const response = await client.get(`/api/compare?models=${ids}`);
      setCompareData(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to compare models.');
    } finally {
      setIsComparing(false);
    }
  };

  const getColor = (modelName) => {
    if (!modelName) return 'var(--color-text-muted)';
    const lowerName = modelName.toLowerCase();
    if (lowerName.includes('gpt')) return 'var(--color-primary)';
    if (lowerName.includes('claude')) return 'var(--color-violet)';
    if (lowerName.includes('gemini')) return 'var(--color-amber)';
    if (lowerName.includes('llama')) return 'var(--color-success)';
    return 'var(--color-text-muted)';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="font-display text-3xl font-bold text-text mb-8">Compare Models</h1>
      
      {/* Selection Area */}
      <div className="bg-surface border border-border rounded-lg p-6 mb-8 shadow-sm">
        <label className="block text-sm font-medium text-text-muted mb-3">
          Select 2 to 4 models to compare
        </label>
        
        <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
          <select 
            onChange={handleSelectModel}
            disabled={isLoadingModels || selectedModels.length >= 4}
            className="w-full sm:w-auto bg-bg border border-divider rounded-md px-4 py-2.5 text-text focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary disabled:opacity-50 min-w-[250px]"
            defaultValue=""
          >
            <option value="" disabled>-- Select a model --</option>
            {models?.map(m => (
              <option key={m.id} value={m.id} disabled={selectedModels.some(sel => sel.id === m.id)}>
                {m.name}
              </option>
            ))}
          </select>
          
          <button
            onClick={handleCompare}
            disabled={selectedModels.length < 2 || isComparing}
            className="w-full sm:w-auto px-6 py-2.5 bg-primary text-bg font-medium rounded-md hover:bg-primary-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isComparing ? 'Comparing...' : 'Compare'}
          </button>
        </div>

        {error && <p className="text-error text-sm mt-3">{error}</p>}

        {/* Selected Chips */}
        <div className="flex flex-wrap gap-2 mt-5">
          {selectedModels.map(m => (
            <div key={m.id} className="flex items-center gap-2 bg-surface-2 border border-divider px-3 py-1.5 rounded-full">
              <span className="text-sm font-medium text-text">{m.name}</span>
              <button 
                onClick={() => handleRemoveModel(m.id)}
                className="text-text-faint hover:text-error focus:outline-none"
                title="Remove model"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Results Area */}
      {isComparing && (
        <div className="compare-charts grid grid-cols-1 lg:grid-cols-2 gap-8 animate-pulse">
          <div className="h-[400px] bg-surface rounded-lg border border-border"></div>
          <div className="h-[400px] bg-surface rounded-lg border border-border"></div>
        </div>
      )}

      {compareData && !isComparing && (
        <div className="compare-charts grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Chart: Radar */}
          <div>
            <h3 className="font-display text-lg font-bold text-text mb-4 text-center">Multi-Dimensional View</h3>
            <RadarChart models={compareData.models} data={compareData.radar_data} />
          </div>
          
          {/* Right Chart: Bar */}
          <div>
            <h3 className="font-display text-lg font-bold text-text mb-4 text-center">Benchmark Comparison</h3>
            <div className="w-full h-[400px] bg-bg rounded-lg border border-border p-4 shadow-sm">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={compareData.radar_data} margin={{ top: 20, right: 10, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--color-divider)" vertical={false} />
                  <XAxis 
                    dataKey="benchmark" 
                    stroke="var(--color-text-faint)" 
                    tick={{ fill: 'var(--color-text-muted)', fontSize: 12 }} 
                  />
                  <YAxis 
                    stroke="var(--color-text-faint)" 
                    tick={{ fill: 'var(--color-text-muted)', fontSize: 12 }} 
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'var(--color-surface-2)', 
                      borderColor: 'var(--color-border)', 
                      color: 'var(--color-text)',
                      borderRadius: 'var(--radius-md)'
                    }}
                    itemStyle={{ color: 'var(--color-text)' }}
                  />
                  <Legend wrapperStyle={{ color: 'var(--color-text-muted)', paddingTop: '10px' }} />
                  
                  {compareData.models.map(modelName => (
                    <Bar 
                      key={modelName} 
                      dataKey={modelName} 
                      fill={getColor(modelName)} 
                      radius={[4, 4, 0, 0]}
                      isAnimationActive={true}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Compare;
