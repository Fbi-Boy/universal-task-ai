# Approval decision security

Approval-required tool executions are durable and fail closed.

## Rules

- Every approval decision requires a non-empty actor identifier bounded to 128 characters.
- The approval store persists the decision actor and UTC decision timestamp.
- Approval decisions are one-way: pending -> approved/rejected, then approved -> consumed.
- A rejected or consumed approval cannot be reused.
- Existing approval databases are migrated in place by adding nullable decision metadata columns.
- Invocation arguments remain excluded from approval execution metadata responses.

## API

Approval endpoints require the normal authenticated API boundary. Decision requests provide an actor_id; the value is recorded as decision metadata and is not treated as a permission grant.

The runtime still revalidates the stored approval, run ID, task ID, plan ID, and tool boundary before execution. Approval state never grants a new tool or capability.