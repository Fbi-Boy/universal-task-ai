#!/usr/bin/env bash
set -euo pipefail

if [[ ! -x .venv/bin/python ]]; then
  echo "Missing .venv. Create it with: python3 -m venv .venv" >&2
  exit 1
fi

".venv/bin/python" scripts/check-local.py
exec ".venv/bin/python" -m uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --env-file .env
