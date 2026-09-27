$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    Write-Error "Missing .venv. Create it with: python -m venv .venv"
}

& ".\.venv\Scripts\python.exe" -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --env-file .env
