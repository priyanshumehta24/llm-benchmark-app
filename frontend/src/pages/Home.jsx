import { useEffect, useRef } from 'react'

const MODELS = [
  { name: 'GPT-5',          family: 'GPT',    provider: 'OpenAI',    open: false },
  { name: 'Claude 4',       family: 'Claude', provider: 'Anthropic', open: false },
  { name: 'Gemini 2.5 Pro', family: 'Gemini', provider: 'Google',    open: false },
  { name: 'Llama 4',        family: 'Llama',  provider: 'Meta',      open: true  },
  { name: 'DeepSeek V3',    family: 'DS',     provider: 'DeepSeek',  open: true  },
  { name: 'Mistral Large',  family: 'Ms',     provider: 'Mistral',   open: false },
]

const STATS = [
  { value: '9',   label: 'Models Tracked' },
  { value: '10+', label: 'Benchmarks' },
  { value: '6',   label: 'Use Cases' },
  { value: '24h', label: 'Auto-Update' },
]

export default function Home() {
  const heroRef = useRef(null)

  useEffect(() => {
    // Stagger animation on mount
    const cards = heroRef.current?.querySelectorAll('.stat-card')
    cards?.forEach((card, i) => {
      card.style.animationDelay = `${i * 80}ms`
      card.classList.add('animate-fade-up')
    })
  }, [])

  return (
    <main style={{ flex: 1, padding: '3rem 2rem', maxWidth: '1280px', margin: '0 auto', width: '100%' }}>

      {/* ── Hero ── */}
      <section style={{ textAlign: 'center', paddingBottom: '4rem', animation: 'fadeSlideUp 0.6s ease forwards' }}>
        <div style={{ marginBottom: '1rem' }}>
          <span className="badge badge-cyan">↑ Updated every 24 hours</span>
        </div>

        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(2.2rem, 5vw, 3.8rem)',
          fontWeight: '700',
          letterSpacing: '-0.03em',
          lineHeight: '1.1',
          marginBottom: '1.25rem',
        }}>
          Find the best LLM
          <br />
          <span className="gradient-text">for your exact use case</span>
        </h1>

        <p style={{
          fontSize: '1.1rem',
          color: 'var(--color-text-muted)',
          maxWidth: '560px',
          margin: '0 auto 2rem',
          lineHeight: '1.7',
        }}>
          Aggregated benchmark scores for GPT-5, Claude 4, Gemini 2.5 Pro, Llama 4 and more —
          with AI-powered recommendations tailored to your workflow.
        </p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <a href="/recommend" className="btn-primary">
            ✦ Get a Recommendation
          </a>
          <a href="/compare" className="btn-ghost">
            Compare Models →
          </a>
        </div>
      </section>

      {/* ── Stats ── */}
      <section ref={heroRef} style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
        gap: '1rem',
        marginBottom: '4rem',
      }}>
        {STATS.map(({ value, label }) => (
          <div key={label} className="card stat-card" style={{ textAlign: 'center', opacity: 0 }}>
            <div style={{
              fontFamily: 'var(--font-display)',
              fontSize: '2rem',
              fontWeight: '700',
              color: 'var(--color-primary)',
              marginBottom: '0.25rem',
            }}>{value}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--color-text-muted)' }}>{label}</div>
          </div>
        ))}
      </section>

      {/* ── Models Grid ── */}
      <section>
        <h2 style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.4rem',
          fontWeight: '600',
          marginBottom: '1.5rem',
          color: 'var(--color-text)',
        }}>
          Tracked Models
        </h2>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
          gap: '1rem',
        }}>
          {MODELS.map((model) => (
            <div key={model.name} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {/* Avatar + name */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{
                  width: '40px', height: '40px',
                  borderRadius: 'var(--radius-md)',
                  background: 'linear-gradient(135deg, var(--color-surface-offset), var(--color-surface-2))',
                  border: '1px solid var(--color-border)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: 'var(--font-display)',
                  fontWeight: '700',
                  fontSize: '0.8rem',
                  color: 'var(--color-primary)',
                }}>
                  {model.family.slice(0, 2).toUpperCase()}
                </div>
                <div>
                  <div style={{ fontFamily: 'var(--font-display)', fontWeight: '600', fontSize: '0.95rem' }}>
                    {model.name}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>
                    {model.provider}
                  </div>
                </div>
              </div>

              {/* Badges */}
              <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                <span className={`badge badge-${model.open ? 'green' : 'violet'}`}>
                  {model.open ? '🔓 Open Source' : '🔒 Closed'}
                </span>
              </div>

              {/* Placeholder score bar — animated in Phase 7 */}
              <div style={{
                height: '4px',
                borderRadius: 'var(--radius-full)',
                background: 'var(--color-surface-offset)',
                overflow: 'hidden',
              }}>
                <div style={{
                  height: '100%',
                  width: `${60 + Math.random() * 35}%`,
                  background: 'linear-gradient(90deg, var(--color-primary), var(--color-violet))',
                  borderRadius: 'var(--radius-full)',
                  transition: 'width 0.8s ease',
                }} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Use-case CTA ── */}
      <section style={{
        marginTop: '4rem',
        padding: '2.5rem',
        background: 'var(--color-surface)',
        borderRadius: 'var(--radius-xl)',
        border: '1px solid var(--color-border)',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Decorative glow */}
        <div style={{
          position: 'absolute', inset: 0,
          background: 'radial-gradient(ellipse at 50% 0%, rgba(0,212,255,0.06) 0%, transparent 70%)',
          pointerEvents: 'none',
        }} />

        <h2 style={{
          fontFamily: 'var(--font-display)',
          fontSize: '1.6rem',
          fontWeight: '700',
          marginBottom: '0.75rem',
        }}>
          Not sure which model to use?
        </h2>
        <p style={{ color: 'var(--color-text-muted)', marginBottom: '1.5rem', maxWidth: '480px', margin: '0 auto 1.5rem' }}>
          Describe your task in plain English and our scoring engine will rank models by suitability.
        </p>
        <a href="/recommend" className="btn-primary">Try the Recommendation Engine →</a>
      </section>

    </main>
  )
}
