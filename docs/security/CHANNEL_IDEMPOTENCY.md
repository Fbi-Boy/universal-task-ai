# Channel Idempotency Boundary

Inbound channel events must not create duplicate task executions when providers retry delivery. This store provides a bounded claim keyed by a provider-derived event identifier.

Security rules:
- Keys and result identifiers are length-bounded.
- Duplicate delivery within the TTL is rejected.
- Expired claims may be replaced.
- The store does not grant permissions; normal authentication, authorization, approval, audit, and task execution controls still apply.
- Production persistence should use the durable run-state database rather than process memory.
