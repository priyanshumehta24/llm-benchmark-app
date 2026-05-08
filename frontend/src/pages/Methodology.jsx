import React from 'react';
import { useQuery } from '@tanstack/react-query';
import client from '../api/client';

const Methodology = () => {
  const { data: usecases, isLoading } = useQuery({
    queryKey: ['usecases'],
    queryFn: async () => {
      const response = await client.get('/api/usecases');
      return response.data;
    }
  });

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="font-display text-3xl md:text-4xl font-bold text-text mb-8">
        How Scores Are Calculated
      </h1>

      {/* Section 1: Formula */}
      <section className="mb-12 bg-surface border border-border rounded-lg p-6 sm:p-8 shadow-sm">
        <h2 className="text-xl font-display font-bold text-primary mb-4">Scoring Formula</h2>
        <p className="text-text-muted mb-4 leading-relaxed">
          To ensure fairness across completely different scales (like percentages vs Elo ratings), we normalize every raw score against the maximum score observed for that specific benchmark.
        </p>
        <div className="bg-bg border border-divider rounded-md p-4 mb-6 font-mono text-sm sm:text-base text-violet overflow-x-auto shadow-inner">
          NormalizedScore = RawScore / MaxScoreAcrossAllModels
        </div>
        <p className="text-text-muted mb-4 leading-relaxed">
          Then, each use case has a tailored set of weights depending on its complexity and requirements. The final score is the sum of these weighted normalized scores.
        </p>
        <div className="bg-bg border border-divider rounded-md p-4 font-mono text-sm sm:text-base text-success overflow-x-auto shadow-inner">
          FinalScore = Σ (Weight × NormalizedScore)
        </div>
      </section>

      {/* Section 2: Weight Table */}
      <section className="mb-12">
        <h2 className="text-2xl font-display font-bold text-text mb-6">Weight Tables by Use Case</h2>
        {isLoading ? (
          <div className="animate-pulse space-y-6">
            <div className="h-10 bg-surface rounded w-1/3"></div>
            <div className="h-40 bg-surface rounded"></div>
          </div>
        ) : (
          <div className="space-y-8">
            {usecases?.map(uc => (
              <div key={uc.id} className="bg-surface border border-border rounded-lg overflow-hidden shadow-sm">
                <div className="bg-surface-2 px-6 py-4 border-b border-divider flex items-center gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded bg-primary/10 text-primary flex items-center justify-center">
                    <span className="material-icons text-sm uppercase font-bold">{uc.icon.charAt(0)}</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-text">{uc.label}</h3>
                    <p className="text-sm text-text-faint mt-1">{uc.description}</p>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm text-text-muted">
                    <thead className="bg-bg text-xs uppercase text-text-faint border-b border-divider">
                      <tr>
                        <th className="px-6 py-3 font-medium whitespace-nowrap">Benchmark</th>
                        <th className="px-6 py-3 font-medium whitespace-nowrap">Weight</th>
                        <th className="px-6 py-3 font-medium">Why It Matters</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-divider">
                      {Object.entries(uc.weights).map(([benchmark, weight]) => (
                        <tr key={benchmark} className="hover:bg-surface-offset transition-colors">
                          <td className="px-6 py-4 font-medium text-text whitespace-nowrap">{benchmark}</td>
                          <td className="px-6 py-4 text-amber font-mono whitespace-nowrap">{(weight * 100).toFixed(0)}%</td>
                          <td className="px-6 py-4 italic text-text-faint">
                            A critical metric tailored for {uc.label.toLowerCase()} performance.
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Section 3: Data Sources */}
      <section className="mb-12">
        <h2 className="text-2xl font-display font-bold text-text mb-6">Data Sources</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a href="https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard" target="_blank" rel="noreferrer" className="block bg-surface border border-border rounded-lg p-5 hover:border-primary transition-colors group shadow-sm">
            <h3 className="font-bold text-text group-hover:text-primary transition-colors">Hugging Face Open LLM Leaderboard</h3>
            <p className="text-sm text-text-muted mt-2">MMLU, ARC, HellaSwag, TruthfulQA, Winogrande</p>
          </a>
          <a href="https://paperswithcode.com/api/v1" target="_blank" rel="noreferrer" className="block bg-surface border border-border rounded-lg p-5 hover:border-violet transition-colors group shadow-sm">
            <h3 className="font-bold text-text group-hover:text-violet transition-colors">Papers With Code</h3>
            <p className="text-sm text-text-muted mt-2">GSM8K, HumanEval, MATH</p>
          </a>
          <a href="https://chat.lmsys.org" target="_blank" rel="noreferrer" className="block bg-surface border border-border rounded-lg p-5 hover:border-amber transition-colors group shadow-sm">
            <h3 className="font-bold text-text group-hover:text-amber transition-colors">LMSYS Chatbot Arena</h3>
            <p className="text-sm text-text-muted mt-2">Human preference Elo ratings</p>
          </a>
          <a href="https://ai.google.dev" target="_blank" rel="noreferrer" className="block bg-surface border border-border rounded-lg p-5 hover:border-success transition-colors group shadow-sm">
            <h3 className="font-bold text-text group-hover:text-success transition-colors">Gemini API</h3>
            <p className="text-sm text-text-muted mt-2">Used for natural language use-case classification</p>
          </a>
        </div>
      </section>
    </div>
  );
};

export default Methodology;
