import { Routes, Route } from 'react-router-dom';

const Home = () => <div className="p-8 text-center"><h2 className="font-display text-2xl text-primary">Home</h2><p className="text-text-muted mt-2">Routing active.</p></div>;
const Compare = () => <div className="p-8 text-center"><h2 className="font-display text-2xl text-violet">Compare</h2></div>;
const Recommend = () => <div className="p-8 text-center"><h2 className="font-display text-2xl text-amber">Recommend</h2></div>;
const Methodology = () => <div className="p-8 text-center"><h2 className="font-display text-2xl text-success">Methodology</h2></div>;

function App() {
  return (
    <div className="min-h-screen bg-bg text-text font-body">
      <header className="border-b border-border bg-surface p-4 flex gap-4">
        <h1 className="font-display text-primary text-xl font-bold">LLM Benchmark Analyzer</h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/compare" element={<Compare />} />
          <Route path="/recommend" element={<Recommend />} />
          <Route path="/methodology" element={<Methodology />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
