# WhatsApp Provider Contract

The provider receives an injected SecretProvider and HTTP client. Access tokens never enter task payloads or ordinary application state. Production transport must enforce HTTPS, bounded request/response sizes, timeouts, retry limits, and provider-specific authentication semantics.