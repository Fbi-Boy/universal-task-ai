# Universal Task AI

Secure, modular, hybrid AI assistant for planning, executing, reviewing, and delivering complex tasks across web and local environments.

## Status

The repository has a security-first core, planning pipeline, sandboxed execution, persistent run state, semantic memory, web UI, authenticated APIs, external web search, production container hardening, secret management, and integration/security CI.

The remaining roadmap milestone is an actual production rollout against configured infrastructure. The repository currently contains the protected deployment workflow and a passing ephemeral production rehearsal; a rehearsal is not treated as a real production deployment.

## Product roadmap

See [Premium Product Roadmap](docs/PREMIUM_PRODUCT_ROADMAP.md) for workstream completion estimates, detailed sub-tasks, acceptance criteria, and the remaining production go-live checklist. Percentages are explicitly marked as planning estimates until verified by tests and review.

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
python scripts/setup_local.py
pytest
```

The setup helper creates `.env` with a fresh random API key and refuses to overwrite an existing configuration. It never displays the key. Then launch with `scripts/run-local.ps1` on Windows or `bash scripts/run-local.sh` on Linux/macOS. See [Secure local setup](docs/LOCAL_SETUP.md) for the full workflow and optional local/browser capability configuration.

For the first safe automation path, enter `Hitung: 12 * (3 + 1)` or `Calculate: 12 * (3 + 1)` and leave the tool selector on **Auto — safe intents only**. Only explicit arithmetic expressions are routed automatically; browser, filesystem, and other tools are never inferred or enabled by this shortcut.

Never commit `.env`, API keys, provider tokens, cookies, or sandbox credentials.

## Production

Production deployment is intentionally protected by a GitHub Environment and required deployment secrets. See `docs/operations/PRODUCTION_DEPLOYMENT.md` for the deployment boundary and rehearsal details.

Do not mark production as deployed until a real target has been configured and a successful rollout has been verified.


## AI Agent Program, Governance & Product Blueprint

New agents must read [AGENTS.md](AGENTS.md) and the [Agent Program Workbook](docs/agent-program/README.md) before working. The workbook defines the active AI team size, workstreams, dependencies, contracts, ticket format, coordination process, quality gates and Sprint 0 runbook.

- [Agent Program Workbook](docs/agent-program/README.md) — operational team plan, how many AI sessions to run, workstream owners, dependency map, templates, contract register, backlog, risk register and Sprint 0 steps.
- [Agent Operating System](docs/agent-system/AGENT_OPERATING_SYSTEM.md) — A0–A13 ownership, mandatory startup rules, G0–G6 gates, security, quality, sprint coordination and specialist prompts.
- [Product & Engineering Blueprint](docs/agent-system/PRODUCT_BLUEPRINT.md) — product vision, current-state caveats, architecture, domain map, data/API contracts, and delivery sequence.
- [Design Reference Board](docs/agent-system/DESIGN_REFERENCE_BOARD.html) — screenshot gallery with original source links. Open in a browser with internet access; treat as research, not page approval.
- [Design Reference Matrix](docs/agent-system/DESIGN_REFERENCE_MATRIX.md) — reference/behavior mapping for dashboard, AI workspace, task management, campus, automations, diagrams and billing.

Visual pages require a page-specific screenshot board and explicit owner approval before production UI implementation. Check the live branch, code and CI each sprint; documentation does not mean a planned feature has shipped.
