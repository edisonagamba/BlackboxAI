import { useState } from "react";
import { analyzeLogs } from "../../services/chatApi";
import "./LogAnalyzer.css";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function LogAnalyzer() {
  const [logs, setLogs] = useState("");
  const [context, setContext] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    if (!logs.trim()) return;

    setLoading(true);
    setError("");
    setAnalysis("");

    try {
      const result = await analyzeLogs({
        logs: logs.split("\n").filter(Boolean),
        context: context.trim() || null,
      });

      setAnalysis(result.analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="analyzer">
      <div className="analyzer-grid">
        <div className="input-column">
          <div className="field field-context">
            <div className="field-heading">
              <label htmlFor="context">Incident context</label>
              <span>Optional</span>
            </div>
            <textarea
              id="context"
              value={context}
              onChange={(event) => setContext(event.target.value)}
              placeholder="What happened? Include affected service, environment, or timeline..."
            />
          </div>

          <div className="field field-logs">
            <div className="field-heading">
              <label htmlFor="logs">Application logs</label>
              <span>{logs.length.toLocaleString()} chars</span>
            </div>
            <textarea
              id="logs"
              value={logs}
              onChange={(event) => setLogs(event.target.value)}
              placeholder={"Paste stack traces or application logs here...\n\n2026-11-23 14:32:01 ERROR [orders] Request failed"}
            />
          </div>
        </div>

        <aside className="guide-card">
          <div className="guide-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none">
              <path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" />
              <circle cx="12" cy="12" r="4" stroke="currentColor" strokeWidth="1.7" />
            </svg>
          </div>
          <h2>For the strongest analysis</h2>
          <ul>
            <li><span>01</span>Include the relevant time range</li>
            <li><span>02</span>Add the affected service or endpoint</li>
            <li><span>03</span>Keep logs in chronological order</li>
          </ul>
        </aside>
      </div>

      <div className="action-row">
        {logs && (
          <button className="clear-button" type="button" onClick={() => { setLogs(""); setContext(""); setAnalysis(""); setError(""); }}>
            Clear
          </button>
        )}
        <button
          className="analyze-button"
          type="button"
          onClick={handleAnalyze}
          disabled={loading || !logs.trim()}
        >
          {loading ? (
            <>
              <span className="spinner" aria-hidden="true" />
              Analyzing logs
            </>
          ) : (
            <>
              Analyze logs
              <svg viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M4 10h12M11.5 5.5 16 10l-4.5 4.5" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="error" role="alert">
          <span aria-hidden="true">!</span>
          <div><strong>Analysis failed</strong><p>{error}</p></div>
        </div>
      )}

      {analysis && (
        <section className="results">
          <div className="results-header">
            <div>
              <p className="eyebrow">Completed</p>
              <h2>Analysis results</h2>
            </div>
            <span className="confidence">AI generated</span>
          </div>
          <div className="markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{analysis}</ReactMarkdown>
          </div>
        </section>
      )}
    </section>
  );
}
