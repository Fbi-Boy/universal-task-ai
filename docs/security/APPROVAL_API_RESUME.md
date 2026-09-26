# Approval API and Durable Resume Contract

## Scope
The approval API is authenticated at the application router boundary. Approval state and tool invocation payloads are persisted in SQLite.

## Resume flow
1. Task execution persists a bounded contract/plan manifest while entering `WAITING_APPROVAL`.
2. An operator approves the persisted approval.
3. The authenticated resume endpoint receives `run_id`, `approval_id`, and bounded `actor_id`.
4. The service reconstructs the contract and plan from the durable run manifest.
5. The approval store atomically consumes the approval.
6. Only then may the configured `RuntimeToolBoundary` execute the stored invocation.
7. A second resume cannot consume the same approval.

## Security requirements
- Path and body approval IDs must match.
- Actor IDs are limited to 128 characters.
- Missing task service returns 503 rather than silently executing.
- Missing approval store or tool boundary fails closed.
- Durable manifests are validated with strict Pydantic models.
- Tool invocation bounds are revalidated after persistence.
- Audit metadata recursively redacts common secret-bearing keys.
- Exactly-once approval consumption does not imply exactly-once external side effects.

## Runtime wiring
The FastAPI runtime uses the same persistent approval database path as the production compose environment via `UTA_APPROVAL_DB`. The task service is placed in application state so the approval router can invoke the controlled resume path without importing the application module.

## Validation
CI must pass unit tests, integration/security checks, Python compilation, dependency audit, and production rehearsal before merge.
