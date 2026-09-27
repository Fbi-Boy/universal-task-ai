# API Hardening

## Controls

- Every HTTP response receives a bounded correlation identifier through X-Request-ID.
- Caller-provided request identifiers are accepted only when printable ASCII and at most 128 characters.
- Invalid identifiers are replaced with a cryptographically random 128-bit identifier.
- Requests larger than the configured body limit are rejected before application parsing.
- Streaming bodies are counted as they arrive; the default limit is 1 MiB.
- Oversize failures use HTTP 413 and Cache-Control: no-store.
- Correlation identifiers are metadata only; they grant no authentication or runtime capability.

## Security boundary

Request IDs are never treated as identity, permission, approval, or authorization. Authentication remains the existing bearer API-key boundary.
