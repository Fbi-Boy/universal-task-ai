# Local Setup

Universal Task AI is local-first and least-privilege by default. Browser, local filesystem, and Python sandbox capabilities are opt-in.

## Quick start

See the detailed [Secure local setup guide](../LOCAL_SETUP.md) for Windows and Linux/macOS commands.

1. Create a Python 3.11+ virtual environment.
2. Install development dependencies: `pip install -e ".[dev]"`.
3. Copy `.env.example` to `.env`.
4. Generate a random key with `python -c "import secrets; print(secrets.token_urlsafe(32))"` and set `UNIVERSAL_TASK_AI_API_KEY` in `.env`.
5. Run `.scriptsun-local.ps1` on Windows or `bash scripts/run-local.sh` on Linux/macOS.

The launchers run a fail-closed preflight before starting the API and bind Uvicorn to `127.0.0.1`. The preflight rejects missing/short API keys, incomplete browser allowlist configuration, and unpinned sandbox images. It never prints the key value. The Windows launcher explicitly stops when the preflight returns a non-zero exit code.

## Capability policy

- Browser execution is disabled by default unless `UTA_BROWSER_ENABLED=true` and a narrow `UTA_BROWSER_ALLOWED_HOSTS` allowlist is configured.
- Local filesystem access is disabled by default; when enabled it requires explicit `UTA_LOCAL_ROOTS` roots and remains read-only.
- Python sandbox execution is disabled by default unless explicitly enabled and requires an immutable image digest such as `@sha256:<64-hex-digest>`.
- High-risk browser and tool actions remain approval-gated by the runtime policy.

## Verification

- `/health` is a liveness check.
- `/ready` verifies runtime readiness.
- Run `pytest` before enabling additional capabilities.

Never commit `.env`, API keys, provider tokens, cookies, or sandbox credentials.
