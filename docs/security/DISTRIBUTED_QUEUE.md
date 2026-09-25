# Distributed queue security contract

The production job queue is Redis-backed and uses TLS-only `rediss://` configuration.

The queue:
- stores JSON data, never executable objects
- has atomic bounded enqueue capacity
- enforces per-job payload limits
- uses atomic ready-to-processing movement for multiple workers
- requires explicit acknowledgement
- rejects non-TLS Redis URLs
- validates claim timeout bounds

A production deployment must provide Redis over TLS and keep its connection credential outside task input. Queue credentials are deployment configuration, not model-controlled tool arguments.

The queue is deliberately not a replacement for run-state persistence: the existing run state store remains the source of durable execution state.
