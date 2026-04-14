#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "Error: uvicorn is not installed. Install Python dependencies first: pip install -r requirements.txt" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm is not installed. Install Node.js and npm first." >&2
  exit 1
fi

echo "Starting backend: http://127.0.0.1:8000"
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000 &
backend_pid=$!

cd frontend

echo "Starting frontend: http://127.0.0.1:5173"
npm run dev -- --host 0.0.0.0 &
frontend_pid=$!

cleanup() {
  echo "Shutting down frontend and backend..."
  kill "$backend_pid" "$frontend_pid" >/dev/null 2>&1 || true
  wait "$backend_pid" "$frontend_pid" 2>/dev/null || true
}

trap cleanup EXIT INT TERM
wait "$backend_pid" "$frontend_pid"