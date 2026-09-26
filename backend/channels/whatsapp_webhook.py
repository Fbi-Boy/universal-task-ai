from dataclasses import dataclass
from backend.channels.whatsapp_security import verify_challenge

@dataclass(frozen=True)
class WebhookResponse:
    status: int
    body: str

class WhatsAppWebhook:
    def __init__(self, expected_token: str):
        self.expected_token = expected_token

    def challenge(self, token: str, challenge: str):
        try:
            verified = verify_challenge(token, self.expected_token, challenge)
        except PermissionError:
            return WebhookResponse(403, "forbidden")
        return WebhookResponse(200, verified)

    def receive(self, inbound_adapter, body: bytes, signature: str):
        return inbound_adapter.authenticate_inbound(body, signature)
