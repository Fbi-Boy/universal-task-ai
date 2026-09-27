# Runtime Readiness

The /ready endpoint is a dependency readiness probe, not a liveness endpoint.

It verifies:

- run-state SQLite is responsive;
- durable approval SQLite is responsive;
- audit SQLite is responsive.

A failed dependency returns HTTP 503 with a generic message and does not expose database errors or secret configuration.

The /health endpoint remains a lightweight public liveness/build-identity endpoint. Readiness performs no task execution, model invocation, browser action, filesystem action, or external network request.
