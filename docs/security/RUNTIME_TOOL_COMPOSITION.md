# Runtime Tool Composition

## Security contract

The API may accept structured tool invocations, but accepting a tool name does not grant capability. Every invocation must pass through RuntimeToolBoundary, which enforces registry membership and the configured capability policy.

The default runtime currently registers only the bounded calculator tool. It grants no network, filesystem, or process capability.

## Bounds

- Maximum 8 tool invocations per task.
- Each ToolInvocation revalidates its argument count, key size, nesting depth, and scalar size.
- Unknown tools fail closed.
- Tool execution is never performed by direct registry access.
- Approval-required execution continues to use the durable approval store and resume boundary.

## Audit

Runtime execution receives a persistent SQLite audit sink. Audit metadata is sanitized before persistence so common secret-bearing fields are removed recursively.

## Extension rule

Adding a new runtime tool requires:
1. explicit registry registration;
2. explicit permission capability;
3. tool-specific bounds;
4. unit and integration tests;
5. threat-model/security documentation;
6. approval requirements for side effects.

No network, filesystem, or process capability is enabled merely by adding a tool class.
