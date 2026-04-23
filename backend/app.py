from pathlib import Path
import sys
import os
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from jose import JWTError, jwt

from src.sourcesync.analyzer.parser import analyze_candidate
from src.sourcesync.main import run_xray_search
from src.sourcesync.database.mongo_db import MongoDBClient

class AnalyzeRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    text: str

class UserRegister(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# DB client
db = MongoDBClient(uri=os.getenv("MONGO_URI", "mongodb://localhost:27017"))

# Security
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI(title="SourceSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/register")
def register(user: UserRegister):
    if db.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = db.hash_password(user.password)
    db.insert_user(user.email, hashed)
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    db_user = db.get_user_by_email(user.email)
    if not db_user or not db.verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

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
def analyze(request: AnalyzeRequest, current_user: str = Depends(get_current_user)):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required.")
    return analyze_candidate(request.text)

@app.post("/xray-search")
def xray_search(request: SearchRequest, current_user: str = Depends(get_current_user)):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Job description text is required.")

    parsed = analyze_candidate(request.text)
    try:
        results = run_xray_search(parsed)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"X-ray search failed: {exc}")

    return {"parsed_keywords": parsed, "results": results}
