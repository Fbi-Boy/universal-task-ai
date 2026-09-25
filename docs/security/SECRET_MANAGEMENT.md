# Secret management boundary

Production credentials are provided as container-mounted secrets under `/run/secrets` and are read through `backend/core/secret_provider.py`.

The provider:
- rejects path traversal in secret names
- prefers mounted secret files
- supports an explicit environment fallback for local development
- never logs or places secret values in task payloads
- keeps secret names application-defined rather than model-controlled

Production Compose mounts the API authentication key and external search credential as Docker secrets. Local `secrets/` files are ignored by Git. No credential values belong in the repository.

The environment fallback remains available for development and compatibility; production deployment should use the mounted secret files.
