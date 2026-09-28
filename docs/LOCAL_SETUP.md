# Secure local setup

This project binds the local API to `127.0.0.1` by default. Keep that loopback binding unless you have deliberately designed and secured a remote deployment.

## Windows PowerShell

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe scripts\setup_local.py
```

The setup helper creates `.env` from the reviewed `.env.example` template and generates a fresh random `UNIVERSAL_TASK_AI_API_KEY`. It does not print the key and refuses to overwrite an existing `.env`. Keep the repository in a private user-owned directory because Windows file permissions inherit from the parent directory.

Then run:

```powershell
.\scripts\run-local.ps1
```

The launcher runs a fail-closed preflight before starting the API. If authentication is missing/weak, browser allowlist configuration is incomplete, or the Python sandbox image is not pinned by digest, the server does not start.

Open `http://127.0.0.1:8000` in your browser. In the UI's Connection panel, enter the same API key for the current browser session. The key is not saved into task text.

## Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/python scripts/setup_local.py
```

The helper creates `.env` with owner-only file permissions (0600) and never prints the generated key. If `.env` already exists, it exits without modifying it. Then run:

```bash
./scripts/run-local.sh
```

The launcher binds only to loopback and stops if preflight fails.

## Optional capabilities

- Local filesystem reads require narrow, explicit `UTA_LOCAL_ROOTS` entries. Access is read-only; do not grant your whole home directory unless that is intentionally required.
- Browser automation remains disabled unless `UTA_BROWSER_ENABLED=true` and `UTA_BROWSER_ALLOWED_HOSTS` is configured with only the hosts you need.
- Python execution remains disabled unless explicitly enabled with a sandbox image pinned by immutable `@sha256:` digest.

## Safe automatic intent routing

The default **Auto — safe intents only** mode recognizes a narrow set of explicit arithmetic prompts such as `Hitung: 12 * (3 + 1)` and `Calculate 2 ** 3`. The expression must fit a strict character and length allowlist and is evaluated by the existing AST-based calculator. Other tasks stay on the safe baseline unless you explicitly choose a registered tool. This feature does not enable browser, filesystem, shell, or process access.

## Verify

In another terminal, run:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_local.py
```

Set `UNIVERSAL_TASK_AI_API_KEY` in that terminal's environment first, or run the smoke test after setting it in the environment used by your shell. The smoke test refuses any `UTA_SMOKE_BASE_URL` that is not an HTTP(S) loopback URL, so it cannot send the API key to a remote host by configuration mistake. A successful local check does not mean the application has been deployed to production.

## Troubleshooting

- **Setup says `.env` already exists:** it is intentionally preserved; edit it carefully or back it up before making changes.
- **Preflight says the API key is missing/weak:** rerun the setup helper only after safely backing up/removing an invalid `.env`, or generate a new random key and update the existing file. Never use a public/example value.
- **Browser preflight fails:** keep browser disabled or set a narrow host allowlist before enabling it.
- **Sandbox preflight fails:** keep Python sandbox disabled or configure an approved immutable image digest.
- **Port 8000 is in use:** stop the other local service or intentionally choose a documented port and update the smoke-test URL; do not expose the API on all interfaces as a workaround.
