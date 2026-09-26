# Runtime Tool Execution

Tool execution is available only through RuntimeToolBoundary. TaskExecutor never calls a registry tool directly.

## Required controls

- Explicit ToolInvocation objects; arbitrary callable references are not accepted.
- Argument count, nesting depth, key length, and scalar size are bounded before execution.
- Registered-tool metadata is rechecked by the runtime boundary for capability and approval requirements.
- Security-relevant lifecycle events are emitted to an injected AuditSink.
- Audit metadata is sanitized before retention.
- Missing runtime boundaries fail closed.

## Failure behavior

A denied or malformed invocation fails the run and emits tool_denied plus task_failed. A tool returning success=false also fails the run.

Approval-gated tool runs persist only the approval id, tool name, execution plan, and SHA-256 hash of the bounded arguments. Raw pending arguments are not stored. Resume requires the persisted run to be WAITING_APPROVAL, the exact approval id, the same tool name, and the same argument hash. The trusted resume path consumes approval internally; approval is never accepted as a tool argument. Replay after the run leaves WAITING_APPROVAL is rejected. Approval-gated runs currently allow exactly one tool invocation.
