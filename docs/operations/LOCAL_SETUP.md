# Local Setup

Universal Task AI runs with a least-privilege tool set by default. Browser, local filesystem, and Python sandbox capabilities are opt-in.

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

## Browser capability

Browser execution is disabled by default. To enable it, install the browser extra and Chromium:

```bash
pip install -e ".[dev,browser]"
python -m playwright install chromium
```

Then set `UTA_BROWSER_ENABLED=true` and a narrow `UTA_BROWSER_ALLOWED_HOSTS` allowlist. Browser actions remain high-risk and approval-gated.

## Local filesystem capability

Set `UTA_LOCAL_ROOTS` to explicit roots only. Windows uses `;`; Linux/macOS use `:`.

## Python sandbox

The Python sandbox remains disabled unless explicitly enabled and requires an immutable image digest:

`UTA_PYTHON_SANDBOX_ENABLED=true`
`UTA_SANDBOX_IMAGE=registry.example/uta-sandbox@sha256:<64-hex-digest>`

## Verification

`/health` is a liveness check. `/ready` verifies that the runtime can be constructed and the configured tool boundary is available. Run `pytest` before enabling additional capabilities.

Never commit `.env`, API keys, provider tokens, or sandbox credentials.
