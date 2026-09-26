# Browser Execution Boundary

A browser session holds only browser state and the current policy. Every initial navigation and redirect is revalidated against the host policy.

The production executor must run in an isolated browser/container with bounded CPU, memory, time, downloads, and filesystem access. Credentials must not be persisted in ordinary task state. Sensitive actions must pause for explicit user approval and emit audit events before resuming.

This module intentionally does not launch a real browser; that runtime belongs behind the boundary.
