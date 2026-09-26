# Runtime Tool Execution

Tool execution is available only through RuntimeToolBoundary. TaskExecutor never calls a registry tool directly.

## Required controls

- Explicit ToolInvocation objects; arbitrary callable references are not accepted.
- Argument count, nesting depth, key length, and scalar size are bounded before execution.
- Registered-tool metadata is rechecked by the runtime boundary for capability and approval requirements.
- Security-relevant lifecycle events are emitted to an injected AuditSink.
- Audit metadata is sanitized before retention.
- Missing runtime boundaries fail closed.
- Approval-required tool stages enter WAITING_APPROVAL before any tool execution.

## Failure behavior

A denied or malformed invocation fails the run and emits tool_denied plus task_failed. A tool returning success=false also fails the run.

Approval is a state-machine concern and must never be smuggled through arbitrary tool arguments.
