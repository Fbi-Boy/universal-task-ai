from backend.channels.base import ChannelAdapter
from backend.core.channel import Channel,InboundMessage,OutboundMessage

class FakeAdapter(ChannelAdapter):
    def authenticate_inbound(self,payload,headers):
        return InboundMessage(Channel.WHATSAPP,"user-1","hello",True,"user-1")
    def send(self,message): self.sent=message

def test_channel_adapter_keeps_identity_and_outbound_target():
    a=FakeAdapter(); m=a.authenticate_inbound(b"{}",{})
    assert m.authenticated and m.external_user_id=="user-1"
    a.send(OutboundMessage(Channel.WHATSAPP,"user-1","approval required"))
    assert a.sent.target=="user-1"
