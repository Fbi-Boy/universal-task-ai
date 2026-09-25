# Universal Task AI

Secure, modular, hybrid AI assistant for planning, executing, reviewing, and delivering complex tasks across web and local environments.

## Status

The repository has a security-first core, planning pipeline, sandboxed execution, persistent run state, semantic memory, web UI, authenticated APIs, external web search, production container hardening, secret management, and integration/security CI.

The remaining roadmap milestone is an actual production rollout against configured infrastructure. The repository currently contains the protected deployment workflow and a passing ephemeral production rehearsal; a rehearsal is not treated as a real production deployment.

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

## Production

Production deployment is intentionally protected by a GitHub Environment and required deployment secrets. See `docs/operations/PRODUCTION_DEPLOYMENT.md` for the deployment boundary and rehearsal details.

Do not mark production as deployed until a real target has been configured and a successful rollout has been verified.
