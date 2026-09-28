$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Error "Missing .venv. Create it with: python -m venv .venv"
}

if (-not (Test-Path ".env")) {
    Write-Error "Missing .env. Copy .env.example to .env and configure UNIVERSAL_TASK_AI_API_KEY."
}

& ".\.venv\Scripts\python.exe" "scripts\check-local.py"
if ($LASTEXITCODE -ne 0) {
    throw "Local security preflight failed (exit code $LASTEXITCODE). Server was not started."
}

& ".\.venv\Scripts\python.exe" -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --env-file .env
