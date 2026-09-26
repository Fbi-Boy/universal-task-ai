from dataclasses import dataclass
from backend.channels.whatsapp_security import verify_webhook_signature

@dataclass(frozen=True)
class WhatsAppInbound:
    external_user_id: str
    text: str
    message_id: str

class WhatsAppInboundAdapter:
    def __init__(self, app_secret: str):
        if not app_secret: raise ValueError("app_secret is required")
        self.app_secret=app_secret
    def authenticate_inbound(self,payload:bytes,headers:dict[str,str])->WhatsAppInbound:
        signature=headers.get("X-Hub-Signature-256","")
        if not verify_webhook_signature(payload,signature,self.app_secret):
            raise PermissionError("invalid webhook signature")
        raise NotImplementedError("provider payload mapping must be implemented at integration boundary")
