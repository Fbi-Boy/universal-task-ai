# Runtime Tool Boundary

All orchestrated tool execution must cross `RuntimeToolBoundary`.

Security rules:

- Only tools already registered in `ToolRegistry` can execute.
- The task permission allowlist must contain the exact tool name.
- Network, filesystem, and process capabilities are checked independently.
- Tools marked `requires_approval` require an explicit approval marker.
- Unknown tools and denied capabilities fail closed.
- Agent runtimes must receive the boundary, not a raw `ToolRegistry`.
- The boundary does not expose shell discovery, dynamic imports, arbitrary callables, or implicit host access.

This boundary is deliberately separate from tool implementation. A future browser, local-agent, research, or programming tool must still satisfy the same policy gate before the orchestrator or an agent can invoke it.
