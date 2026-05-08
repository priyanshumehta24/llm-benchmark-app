import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Compare from './pages/Compare';
import Recommend from './pages/Recommend';
import Methodology from './pages/Methodology';

function App() {
  return (
    <div className="min-h-screen bg-bg text-text font-body flex flex-col">
      <Navbar />
      
      <main className="flex-grow">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/recommend" element={<Recommend />} />
          <Route path="/methodology" element={<Methodology />} />
        </Routes>
      </main>
      
      <footer className="border-t border-border bg-surface py-6 mt-auto">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-text-faint text-sm">
            Data auto-refreshes every 24h &middot; Built with public benchmarks
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
