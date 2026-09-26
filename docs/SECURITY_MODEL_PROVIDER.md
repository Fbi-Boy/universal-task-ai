# Secure model provider boundary

The model provider is an external network boundary. Credentials stay on the server or local runtime and never come from task text, browser code, or tool arguments.

## Current provider

OpenAIModelGateway uses the fixed HTTPS endpoint https://api.openai.com/v1/responses and reads the OpenAI key through the existing SecretProvider.

## Security requirements

- API keys are server-side secrets only.
- The provider endpoint is fixed; callers cannot supply arbitrary URLs.
- Requests are bounded to 256KB and responses to 1MB.
- Network timeout is bounded to 120 seconds.
- Model output is untrusted data and cannot grant tools, permissions, or approvals.
- Non-zero temperature is rejected until provider-specific sampling semantics are explicitly supported.
- Provider errors do not include response bodies.

## Configuration

Provide OPENAI_API_KEY to the server/local runtime through the existing secret mechanism. Do not put it in frontend JavaScript, task text, Git, or Docker images.

OpenAI's official documentation describes API keys as secrets and recommends server-side environment variables or a key-management service.
