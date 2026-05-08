import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Compare from './pages/Compare'
import Recommend from './pages/Recommend'
import Methodology from './pages/Methodology'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,   // 5 min — benchmark data doesn't change frequently
      retry: 2,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <Routes>
            <Route path="/"            element={<Home />} />
            <Route path="/compare"     element={<Compare />} />
            <Route path="/recommend"   element={<Recommend />} />
            <Route path="/methodology" element={<Methodology />} />
          </Routes>
          <footer style={{
            borderTop: '1px solid var(--color-divider)',
            padding: '1.5rem 2rem',
            textAlign: 'center',
            fontSize: '0.8rem',
            color: 'var(--color-text-faint)',
            fontFamily: 'var(--font-body)',
          }}>
            LLMBench · Data from Hugging Face, Papers With Code, LMSYS Arena · Built by Priyanshu
          </footer>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
