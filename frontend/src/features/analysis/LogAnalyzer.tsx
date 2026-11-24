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
      <h2>Log Analysis</h2>

      <div className="field">
        <label htmlFor="context">Incident Context</label>
        <textarea
          id="context"
          value={context}
          onChange={(event) => setContext(event.target.value)}
          placeholder="Describe the incident or application..."
        />
      </div>

      <div className="field">
        <label htmlFor="logs">Application Logs</label>
        <textarea
          id="logs"
          value={logs}
          onChange={(event) => setLogs(event.target.value)}
          placeholder="Paste your application logs here..."
        />
      </div>

      <button
        className="analyze-button"
        onClick={handleAnalyze}
        disabled={loading || !logs.trim()}
      >
        {loading ? "Analyzing..." : "Analyze Logs"}
      </button>

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      {analysis && (
        <section className="results">
          <h3>Analysis Results</h3>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{analysis}</ReactMarkdown>
        </section>
      )}
    </section>
  );
}
