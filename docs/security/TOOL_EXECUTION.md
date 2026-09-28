# Runtime Tool Execution

Tool execution is available only through RuntimeToolBoundary. TaskExecutor never calls a registry tool directly.

## Required controls

- Explicit ToolInvocation objects; arbitrary callable references are not accepted.
- Tool names and argument objects use strict types; argument trees must contain only plain built-in JSON values, even for internal Python callers.
- Custom dict/list/scalar subclasses are rejected to prevent user-defined methods from running during validation.
- Argument count, nesting depth, object-key length, scalar size, numeric range, and aggregate UTF-8 string bytes are bounded before execution.
- Non-finite floating-point values, non-string object keys, arbitrary Python objects, and oversized integers are rejected.
- Tool results are bounded at the runtime boundary (nested values, collection sizes, scalar size, and error length) before they enter task output or downstream stages.
- Registered-tool metadata is rechecked by the runtime boundary for capability and approval requirements.
- Security-relevant lifecycle events are emitted to an injected AuditSink.
- Audit metadata is recursively sanitized and bounded before retention.
- Missing runtime boundaries fail closed.
- Approval-required tool stages enter WAITING_APPROVAL before any tool execution.
- TaskExecutor derives the approval gate from tool metadata as well as the task contract, so a caller cannot disable a tool's approval requirement by omitting `approval_required` from the task request.

## Failure behavior

A denied or malformed invocation fails the run and emits tool_denied plus task_failed. A tool returning success=false also fails the run.

Approval is a state-machine concern and must never be smuggled through arbitrary tool arguments.

## Approval resume integrity

Approval-gated tool manifests are persisted with the waiting run so resume validation can bind the approval to the exact task and plan. The approval store atomically transitions an approved execution to consumed before tool execution, preventing duplicate resume. Execution manifests are bounded and reject common secret-bearing argument fields before persistence.

Resume requests require a non-empty bounded actor identity. The actor is recorded on the approval-consumed and subsequent tool lifecycle audit events.
