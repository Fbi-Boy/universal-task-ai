#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .venv ]]; then
  echo "Missing .venv. Create it with: python3 -m venv .venv" >&2
  exit 1
fi

source .venv/bin/activate
exec uvicorn backend.api.main:app --host 127.0.0.1 --port 8000 --env-file .env
