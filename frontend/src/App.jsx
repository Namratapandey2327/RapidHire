import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function App() {
  const [jdText, setJdText] = useState("");
  const [parsedKeywords, setParsedKeywords] = useState(null);
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

  const performSearch = async () => {
    const data = await callApi("/xray-search", { text: jdText });
    setParsedKeywords(data.parsed_keywords);
    setSearchResults(data.results);
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <h1>SourceSync</h1>
        <p>Paste a job description and get parsed keywords plus X-ray candidate links.</p>
      </header>

      <main>
        <section className="pane">
          <h2>Job Description Input</h2>
          <textarea
            value={jdText}
            placeholder="Paste job description here"
            onChange={(event) => setJdText(event.target.value)}
          />
          <button onClick={performSearch} disabled={!jdText || loading}>
            Generate Keywords & X-ray Links
          </button>
        </section>

        {loading && <div className="notice">Loading…</div>}
        {error && <div className="error">{error}</div>}

        {parsedKeywords && (
          <section className="results">
            <h2>Parsed Keywords</h2>
            <div className="result-grid">
              <div>
                <strong>Job Title</strong>
                <p>{parsedKeywords["Job Title"] || "Undetermined"}</p>
              </div>
              <div>
                <strong>Location</strong>
                <p>{parsedKeywords.Location || "Undetermined"}</p>
              </div>
              <div>
                <strong>Experience</strong>
                <p>{parsedKeywords.Experience || "N/A"}</p>
              </div>
              <div>
                <strong>Visa</strong>
                <p>{parsedKeywords.Visa || "Undetermined"}</p>
              </div>
            </div>
            <div>
              <strong>Skills</strong>
              <p>{parsedKeywords.Skills?.length ? parsedKeywords.Skills.join(", ") : "None detected"}</p>
            </div>
          </section>
        )}

        {searchResults && (
          <section className="results">
            <h2>X-ray Search Links</h2>
            {searchResults.length ? (
              <ul className="search-list">
                {searchResults.map((result, index) => (
                  <li key={index}>
                    <strong>{result.name || "Candidate"}</strong>
                    <p>{result.headline}</p>
                    {result.profile_url ? (
                      <a href={result.profile_url} target="_blank" rel="noreferrer">
                        Open X-ray profile
                      </a>
                    ) : (
                      <span>No profile link available</span>
                    )}
                    <p className="source-label">Source: {result.source}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No X-ray candidates were found for this description.</p>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
