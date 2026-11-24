import LogAnalyzer from "./features/analysis/LogAnalyzer";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="topbar">
        <a className="brand" href="/" aria-label="Blackbox AI home">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3 4.5 7.2v9.6L12 21l7.5-4.2V7.2L12 3Z" stroke="currentColor" strokeWidth="1.8" />
              <path d="m8.2 9.2 3.8 2.2 3.8-2.2M12 11.4v4.7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
            </svg>
          </span>
          <span>Blackbox AI</span>
        </a>
        <div className="topbar-actions">
          <span className="status"><span className="status-dot" /> System operational</span>
        </div>
      </header>

      <main className="workspace">
        <div className="page-heading">
          <div>
            <p className="eyebrow">Incident intelligence</p>
            <h1>Application log analysis</h1>
          </div>
          <p className="heading-copy">
            Investigate errors, identify root causes, and get actionable next steps.
          </p>
        </div>

        <LogAnalyzer />
      </main>
    </div>
  );
}

export default App;