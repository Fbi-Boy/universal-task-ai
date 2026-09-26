# Model Gateway Security Contract

The model gateway is a provider boundary, not a permission boundary.

## Rules

- Model requests use strict Pydantic schemas with forbidden extra fields.
- Requests are bounded to 64 messages and 100,000 total content characters.
- Individual message content is bounded to 16,000 characters.
- Model output is bounded to 20,000 characters.
- Task data is treated as untrusted input.
- Model output never grants tool, filesystem, process, network, credential, or approval capability.
- Tool execution must continue through the RuntimeToolBoundary.
- Providers must be injected explicitly; the core runtime must not discover credentials or endpoints from model output.
- The static provider is the offline deterministic test implementation.

A future local or hosted provider must preserve these limits and add explicit endpoint, credential, timeout, response-size, and network-egress policy.
