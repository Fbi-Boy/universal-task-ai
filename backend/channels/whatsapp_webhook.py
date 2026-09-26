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
        if not verify_challenge(token, self.expected_token, challenge):
            return WebhookResponse(403, "forbidden")
        return WebhookResponse(200, challenge)

    def receive(self, inbound_adapter, body: bytes, signature: str):
        message = inbound_adapter.authenticate_inbound(body, signature)
        return message
