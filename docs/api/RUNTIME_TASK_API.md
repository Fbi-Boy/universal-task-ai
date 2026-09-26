# Runtime Task API Contract

The task API accepts a natural-language task plus an optional bounded list of structured tool invocations.

## Tool invocation

Each invocation contains a tool name and arguments. The API limits a task to eight invocations. The task service revalidates every invocation before planning or execution.

Submitting a tool name is not a capability grant. RuntimeToolBoundary remains authoritative and rejects unregistered tools or tools requiring capabilities that are not enabled.

## Approval

Set approval_required=true for tool execution that must pause for human approval. The task response returns an approval_id while the run is waiting. Approval and resume use the authenticated approval API.

## Runtime construction

The FastAPI application exposes create_app() so tests and controlled deployments can inject a task service. Production construction uses separate persistent paths for run state, approvals, and audit events.

This separation prevents application startup code from becoming the only place where runtime dependencies can be controlled or tested.
