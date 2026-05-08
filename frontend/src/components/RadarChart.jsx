import React from 'react';
import {
  Radar,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip
} from 'recharts';

const RadarChart = ({ models = [], data = [] }) => {
  // Helper to determine color based on model name
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
    <div className="radar-chart-container w-full h-[400px] bg-bg rounded-lg p-2">
      <ResponsiveContainer width="100%" height="100%">
        <RechartsRadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="var(--color-divider)" />
          <PolarAngleAxis 
            dataKey="benchmark" 
            stroke="var(--color-text-faint)" 
            tick={{ fill: 'var(--color-text-muted)', fontSize: 12 }} 
          />
          <PolarRadiusAxis 
            angle={30} 
            domain={[0, 100]} 
            stroke="var(--color-divider)" 
            tick={{ fill: 'var(--color-text-faint)', fontSize: 10 }} 
          />
          
          {models.map((model) => (
            <Radar
              key={model}
              name={model}
              dataKey={model}
              stroke={getColor(model)}
              strokeWidth={2}
              fill="none" /* No fill, stroke only */
              isAnimationActive={true}
            />
          ))}
          
          <Tooltip 
            contentStyle={{ 
              backgroundColor: 'var(--color-surface-2)', 
              borderColor: 'var(--color-border)', 
              color: 'var(--color-text)',
              borderRadius: 'var(--radius-md)'
            }} 
            itemStyle={{ color: 'var(--color-text)' }}
          />
          <Legend 
            wrapperStyle={{ 
              color: 'var(--color-text-muted)',
              paddingTop: '20px' 
            }} 
          />
        </RechartsRadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RadarChart;
