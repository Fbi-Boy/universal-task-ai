# Universal Task AI

Secure, modular, hybrid AI assistant for planning, executing, reviewing, and delivering complex tasks across web and local environments.

## Status
Early foundation phase: contracts, security boundaries, tests, and a minimal API come before powerful execution tools.

## Principles
- Security by design
- Explicit task contracts
- Least privilege
- No unrestricted host execution
- Human approval for risky side effects
- Auditable execution
- Tests before expanding capabilities

## Development
Python 3.11+.

```bash
python -m venv .venv
pip install -e ".[dev]"
pytest
uvicorn backend.api.main:app --reload
```

Copy `.env.example` to `.env`. Never commit secrets.
