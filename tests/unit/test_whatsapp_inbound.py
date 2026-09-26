import pytest
from backend.channels.whatsapp_inbound import WhatsAppInboundAdapter

def test_invalid_signature_rejected_before_payload_parsing():
    with pytest.raises(PermissionError):
        WhatsAppInboundAdapter("secret").authenticate_inbound(b"{}",{"X-Hub-Signature-256":"bad"})
