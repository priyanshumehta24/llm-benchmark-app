import { Link, useLocation } from 'react-router-dom'

const NAV_LINKS = [
  { path: '/',             label: 'Home' },
  { path: '/compare',      label: 'Compare' },
  { path: '/recommend',    label: 'Recommend' },
  { path: '/methodology',  label: 'Methodology' },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav style={{
      background: 'var(--color-surface)',
      borderBottom: '1px solid var(--color-border)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backdropFilter: 'blur(12px)',
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: '0 2rem',
        height: '64px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        {/* Wordmark */}
        <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{
            width: '28px', height: '28px',
            background: 'linear-gradient(135deg, var(--color-primary), var(--color-violet))',
            borderRadius: 'var(--radius-sm)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '14px', fontWeight: '700', color: '#0d0f1a',
          }}>⚡</span>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontWeight: '700',
            fontSize: '1.1rem',
            color: 'var(--color-text)',
            letterSpacing: '-0.02em',
          }}>
            LLM<span style={{ color: 'var(--color-primary)' }}>Bench</span>
          </span>
        </Link>

        {/* Nav links */}
        <div style={{ display: 'flex', gap: '0.25rem' }}>
          {NAV_LINKS.map(({ path, label }) => {
            const isActive = pathname === path
            return (
              <Link
                key={path}
                to={path}
                style={{
                  padding: '0.4rem 0.9rem',
                  borderRadius: 'var(--radius-md)',
                  fontFamily: 'var(--font-display)',
                  fontWeight: '500',
                  fontSize: '0.9rem',
                  color: isActive ? 'var(--color-primary)' : 'var(--color-text-muted)',
                  background: isActive ? 'var(--color-primary-highlight)' : 'transparent',
                  border: isActive ? '1px solid rgba(0,212,255,0.25)' : '1px solid transparent',
                  transition: 'all 0.2s ease',
                  textDecoration: 'none',
                }}
                onMouseEnter={e => {
                  if (!isActive) {
                    e.currentTarget.style.color = 'var(--color-text)'
                    e.currentTarget.style.background = 'var(--color-surface-offset)'
                  }
                }}
                onMouseLeave={e => {
                  if (!isActive) {
                    e.currentTarget.style.color = 'var(--color-text-muted)'
                    e.currentTarget.style.background = 'transparent'
                  }
                }}
              >
                {label}
              </Link>
            )
          })}
        </div>

        {/* Status pill */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: '0.4rem',
          padding: '0.3rem 0.75rem',
          background: 'var(--color-success-highlight)',
          border: '1px solid rgba(74,222,128,0.25)',
          borderRadius: 'var(--radius-full)',
          fontSize: '0.75rem',
          fontFamily: 'var(--font-display)',
          fontWeight: '500',
          color: 'var(--color-success)',
        }}>
          <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--color-success)', animation: 'pulseGlow 2s infinite' }} />
          Live
        </div>
      </div>
    </nav>
  )
}
