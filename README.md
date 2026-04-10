# SourceSync

SourceSync is a candidate intelligence tool built to analyze resumes and candidate summaries for visa status, experience, and technical skills. It also includes X-ray search capabilities to find candidates on LinkedIn based on parsed job requirements.

## Project structure

SourceSync/
├── backend/                # FastAPI backend for React frontend
│   └── app.py              # API endpoints for analysis and X-ray search
├── frontend/               # React frontend application
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       └── index.css
├── src/                    # All source package code
│   └── sourcesync/         # Main Python package
│       ├── __init__.py     # Package entrypoint
│       ├── __main__.py     # Allows running as `python -m sourcesync`
│       ├── analyzer/       # Candidate parsing logic
│       │   ├── __init__.py
│       │   └── parser.py   # Regex and NLP helper functions
│       ├── scraper/        # LinkedIn X-ray search automation
│       │   ├── __init__.py
│       │   ├── engine.py   # Playwright browser automation
│       │   └── selectors.py # Google search DOM selectors
│       └── database/       # Data storage helpers
│           ├── __init__.py
│           └── mongo_db.py # MongoDB connection wrapper
├── tests/                  # Automated tests
│   ├── test_parser.py
│   └── test_scraper.py
├── .env                    # Private credentials (DO NOT COMMIT)
├── .gitignore              # Ignored files for Git
├── backend/                # FastAPI backend for React frontend
│   └── app.py              # API endpoints for analysis and X-ray search
├── test_setup.py          # Setup verification script
├── requirements.txt        # Project dependencies
└── README.md               # This documentation

## Setup & Testing

1. Install system dependencies (Linux):
   ```bash
   sudo apt-get install firefox
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Test your setup:
   ```bash
   python test_setup.py
   ```

## ✅ Setup Verification

Run the test script to verify everything is working:

```bash
python test_setup.py
```

**Expected Results:**
- ✅ Browser works! Page title: Google
- ✅ Parser works! (with sample extracted data)
- ✅ Search works! Found X candidates (may be 0 for test query)

## Run the React + FastAPI UI

1. Start the backend API:
   ```bash
   uvicorn backend.app:app --reload
   ```

2. In another terminal, install frontend dependencies and start the React app:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Open the local Vite preview URL shown in the terminal (usually `http://localhost:5173`).

## Usage Examples

### CLI Analysis
```bash
python -m sourcesync --analyze "5 years experience with Python and AWS"
```

### CLI X-ray Search
```bash
python -m sourcesync --search "Software Engineer Remote MuleSoft OpenShift"
```

## Features

### Candidate Analysis
- **Enhanced Visa Status Detection**: Identifies H1B, Green Card, OPT/CPT, TN Visa, F1 Visa, H4 Visa, and sponsorship needs with robust regex patterns
- **Color-Coded Visa Status**: Visual indicators in the app dashboard (Green for Citizen, Red for H1B/Sponsorship, etc.)
- **Location Detection**: Recognizes Remote, Offshore, Hybrid, Onsite, USA, India
- **Experience Estimation**: Extracts years of experience from text
- **Skill Extraction**: Identifies technical skills from a comprehensive keyword list or pasted sections

### X-ray Search
- **DuckDuckGo Search Integration**: Automated search using DuckDuckGo to find LinkedIn profiles
- **Keyword-Driven**: Uses parsed skills, location, and experience from job descriptions
- **No Credentials Required**: Public search without login requirements
- **LinkedIn Profile Focus**: Filters results to show only LinkedIn professional profiles
- **Smart Search Guards**: Prevents searches when job descriptions lack usable keywords

## Notes

- Keep `.env` private and never commit credentials.
- The scraper uses Playwright with Firefox browser for X-ray search functionality.
- If you encounter browser launch errors, ensure Firefox is installed: `sudo apt-get install firefox`
- Add real selectors and database credentials before using the scraper and storage modules extensively.
