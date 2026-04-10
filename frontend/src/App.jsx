import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function App() {
  const [bioText, setBioText] = useState("");
  const [jdText, setJdText] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const callApi = async (path, body) => {
    setError(null);
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "API request failed.");
      }
      return data;
    } finally {
      setLoading(false);
    }
  };

  const analyzeCandidate = async () => {
    const data = await callApi("/analyze", { text: bioText });
    setAnalysis(data);
    setSearchResults(null);
  };

  const performSearch = async () => {
    const data = await callApi("/xray-search", { text: jdText });
    setAnalysis(data.parsed_keywords);
    setSearchResults(data.results);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>SourceSync</h1>
        <p>React UI for candidate analysis and X-ray search.</p>
      </header>

      <main>
        <section className="pane">
          <h2>Quick Candidate Analysis</h2>
          <textarea
            value={bioText}
            placeholder="Paste candidate About / Experience text here"
            onChange={(event) => setBioText(event.target.value)}
          />
          <button onClick={analyzeCandidate} disabled={!bioText || loading}>
            Analyze Candidate
          </button>
        </section>

        <section className="pane">
          <h2>X-ray Search</h2>
          <textarea
            value={jdText}
            placeholder="Paste job description to extract keywords for X-ray search"
            onChange={(event) => setJdText(event.target.value)}
          />
          <button onClick={performSearch} disabled={!jdText || loading}>
            Perform X-ray Search
          </button>
        </section>

        {loading && <div className="notice">Loading…</div>}
        {error && <div className="error">{error}</div>}

        {analysis && (
          <section className="results">
            <h2>Analysis Results</h2>
            <div className="result-grid">
              <div>
                <strong>Visa Status</strong>
                <p>{analysis.Visa}</p>
              </div>
              <div>
                <strong>Job Title</strong>
                <p>{analysis["Job Title"] || "Undetermined"}</p>
              </div>
              <div>
                <strong>Experience</strong>
                <p>{analysis.Experience}</p>
              </div>
              <div>
                <strong>Location</strong>
                <p>{analysis.Location}</p>
              </div>
            </div>
            <div>
              <strong>Skills</strong>
              <p>{analysis.Skills?.length ? analysis.Skills.join(", ") : "None detected"}</p>
            </div>
          </section>
        )}

        {searchResults && (
          <section className="results">
            <h2>X-ray Search Results</h2>
            {searchResults.length ? (
              <ul className="search-list">
                {searchResults.map((result, index) => (
                  <li key={index}>
                    <strong>{result.name || "Unnamed candidate"}</strong>
                    <p>{result.headline}</p>
                    {result.profile_url && (
                      <a href={result.profile_url} target="_blank" rel="noreferrer">
                        View profile
                      </a>
                    )}
                    <p className="source-label">Source: {result.source}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No candidates found for this search.</p>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
