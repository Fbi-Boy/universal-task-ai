from backend.core.channel import OutboundMessage

class WhatsAppOutboundAdapter:
    def __init__(self, sender):
        self.sender=sender
    def send(self,message:OutboundMessage)->None:
        if not message.recipient_id: raise ValueError("recipient_id is required")
        if not message.text.strip(): raise ValueError("message text is required")
        self.sender(message.recipient_id,message.text)
