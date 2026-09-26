from backend.channels.whatsapp_outbound import WhatsAppOutboundAdapter
from backend.core.channel import Channel,OutboundMessage

def test_outbound_delegates_to_provider_without_authority():
    sent=[]
    a=WhatsAppOutboundAdapter(lambda user,text: sent.append((user,text)))
    a.send(OutboundMessage(Channel.WHATSAPP,"u1","hello"))
    assert sent==[("u1","hello")]
