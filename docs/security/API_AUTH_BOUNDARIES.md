# API Authentication Boundaries

## Task analysis

POST /v1/tasks/analyze is an authenticated API operation. This is intentional even when the deterministic analyzer is enabled because the same endpoint can be backed by an external model provider when model assistance is enabled.

Authentication is enforced by the application route through the existing require_configured_api_key dependency.

## Security requirements

- API credentials are supplied through the existing server-side secret boundary.
- Task text must never contain provider credentials.
- Model-assisted analysis remains untrusted output and cannot grant tools, permissions, approvals, or execution authority.
- /health remains public for liveness/readiness checks and exposes no secret material.
- Tool execution and task submission remain authenticated and separately protected by the runtime capability boundary.

## Regression rule

Any new endpoint that can invoke model providers, consume protected task state, or initiate execution must be explicitly reviewed for authentication before merge.