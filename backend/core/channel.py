from dataclasses import dataclass
from enum import Enum

class Channel(str, Enum):
    WEB='web'
    WHATSAPP='whatsapp'

@dataclass(frozen=True)
class InboundMessage:
    channel: Channel
    external_user_id: str
    text: str
    authenticated: bool = False
    reply_target: str | None = None
    def __post_init__(self):
        if not self.external_user_id.strip(): raise ValueError('external user identity is required')
        if not self.text.strip(): raise ValueError('message text is required')

@dataclass(frozen=True)
class OutboundMessage:
    channel: Channel
    target: str
    text: str
    def __post_init__(self):
        if not self.target.strip(): raise ValueError('outbound target is required')
        if not self.text.strip(): raise ValueError('outbound text is required')
