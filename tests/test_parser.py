from src.sourcesync.analyzer.parser import analyze_candidate

def test_analyze_candidate_detects_visa_and_skills():
    text = "5 years experience with Python, AWS, and React. H1B sponsorship available."
    result = analyze_candidate(text)

    assert result["Visa"] == "H1B/Sponsorship"
    assert "Python" in result["Skills"]
    assert result["Experience"] == "5"

def test_analyze_candidate_returns_undetermined_when_missing_info():
    text = "Entry-level developer with no explicit visa or years listed."
    result = analyze_candidate(text)

    assert result["Visa"] == "Undetermined"
    assert result["Skills"] == []
    assert result["Experience"] == "N/A"
