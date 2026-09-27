# Local model runtime

The local model path uses Ollama through a deliberately narrow loopback-only HTTP boundary.

## Security boundary

- Only `127.0.0.1` and `::1` are accepted; hostname `localhost` is deliberately rejected to avoid hostname-resolution ambiguity.
- The endpoint path is fixed to `/api/chat` and the default Ollama port `11434`.
- HTTPS is not used because this boundary is explicitly local-only; remote hosts are rejected.
- Credentials, query strings, fragments, non-default ports, and redirects are rejected.
- Request and response sizes and network timeout are bounded.
- Model output is untrusted data and is parsed by the strict model-analysis schema.
- The model cannot grant tools, permissions, approvals, credentials, filesystem access, or browser access.

## Configuration

Set `UTA_MODEL_ENABLED=true`, `UTA_MODEL_PROVIDER=ollama`, and `UTA_MODEL=<installed-model>`.
Optionally set `UTA_OLLAMA_BASE_URL`; it must remain a loopback base URL.

If model assistance is disabled, the deterministic analyzer remains the default.
