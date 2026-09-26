# Durable Tool Approval and Resume

## Objective
Approval-required tool execution must stop before any side effect, survive process restarts, and reject duplicate resumes.

## Flow
TaskExecutor -> create execution + approval atomically -> WAITING_APPROVAL -> operator approves -> APPROVED -> atomic consume -> CONSUMED -> RuntimeToolBoundary -> SUCCEEDED / FAILED

The approval identifier is persisted with the run. The invocation payload is bounded before persistence and secret-bearing argument keys are rejected.

## Security requirements
- Tool registry access remains behind RuntimeToolBoundary.
- Approval is a state-machine transition, never a boolean tool argument.
- An approval can be consumed only once.
- A resume request must match the waiting run, task, plan, and approval ID.
- Missing durable approval storage fails closed.
- Secret-bearing argument names are rejected before approval payload persistence.
- Actor identity is recorded in the run state with a bounded length.
- Tool invocation bounds are revalidated after loading from SQLite.

## Failure semantics
Approval consumption happens before tool execution. This prevents duplicate execution after repeated approval callbacks. It also means a process crash after consumption can leave a run requiring recovery from durable run state; the approval itself is intentionally not reusable.

Exactly-once side effects for arbitrary external systems require an idempotency contract at the tool boundary. This component provides exactly-once approval consumption, not a false guarantee about arbitrary external side effects.

## Validation
- persistent approval survives a new ApprovalStore instance
- approved execution transitions to CONSUMED
- repeated consumption is rejected
- secret-bearing arguments are rejected
- executor remains WAITING_APPROVAL before approval
- executor performs the tool once after approval
- repeated resume cannot execute the tool again
- missing durable approval storage fails closed