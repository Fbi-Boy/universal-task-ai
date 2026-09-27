# Local Setup

Universal Task AI is local-first and least-privilege by default. Browser, local filesystem, and Python sandbox capabilities are opt-in.

## Windows PowerShell

1. Create and activate `.venv`.
2. Install development dependencies: `pip install -e ".[dev]"`.
3. Copy `.env.example` to `.env`.
4. Run `.\scripts\run-local.ps1`.

## Linux/macOS

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
bash scripts/run-local.sh
```

The launcher validates `.env` before starting the API and binds Uvicorn to `127.0.0.1`.

## Capability policy

- Browser execution is disabled unless `UTA_BROWSER_ENABLED=true` and a narrow `UTA_BROWSER_ALLOWED_HOSTS` allowlist is configured.
- Local filesystem access requires explicit `UTA_LOCAL_ROOTS` roots and remains read-only.
- Python sandbox execution is disabled unless explicitly enabled and requires an immutable `@sha256:<64-hex-digest>` image reference.
- High-risk browser and tool actions remain approval-gated by the runtime policy.

## Verification

- `/health` is a liveness check.
- `/ready` verifies runtime readiness.
- Run `pytest` before enabling additional capabilities.

Never commit `.env`, API keys, provider tokens, cookies, or sandbox credentials.
