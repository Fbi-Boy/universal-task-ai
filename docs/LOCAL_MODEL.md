# Local model runtime

The local model path uses Ollama through a deliberately narrow loopback-only HTTP boundary.

## Security

- Only `localhost`, `127.0.0.1`, and `::1` are accepted.
- The path is fixed to `/api/chat`.
- Credentials, query strings, and fragments in the endpoint are rejected.
- Request and response sizes are bounded.
- The model receives bounded task context and returns untrusted text.
- Model output cannot grant runtime tools, permissions, approvals, or filesystem/browser access.

This keeps local model inference on the user's machine while preserving the same model gateway contract used by the web deployment.
