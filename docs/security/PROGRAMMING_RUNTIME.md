# Secure Programming Runtime

Python execution is available only as an explicitly enabled runtime capability.

Controls:
- Docker execution uses network=none, read-only root filesystem, dropped capabilities, no-new-privileges, PID/memory/CPU limits, and a bounded timeout.
- Sandbox images must be pinned by an immutable sha256 digest. Mutable tags such as python:3.11 are rejected.
- The Python tool is approval-required and cannot be reached through arbitrary callables.
- The capability is disabled unless UTA_PYTHON_SANDBOX_ENABLED=true and UTA_SANDBOX_IMAGE is supplied.
- The sandbox command is tokenized argv; shell execution is never requested.

This capability is intended for programming/data tasks. A future workspace mount must be separately designed and must not turn the sandbox into unrestricted host filesystem access.
