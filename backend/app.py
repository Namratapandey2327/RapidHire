from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.sourcesync.analyzer.parser import analyze_candidate
from src.sourcesync.main import run_xray_search

class AnalyzeRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    text: str

app = FastAPI(title="SourceSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "SourceSync API is running. Use /health, /analyze, or /xray-search.",
        "endpoints": ["/health", "/analyze", "/xray-search"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required.")
    return analyze_candidate(request.text)

@app.post("/xray-search")
def xray_search(request: SearchRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")

    parsed = analyze_candidate(request.text)
    try:
        results = run_xray_search(parsed)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"X-ray search failed: {exc}")

    return {"parsed_keywords": parsed, "results": results}
