from abc import ABC, abstractmethod
from backend.core.channel import InboundMessage, OutboundMessage

class ChannelAdapter(ABC):
    @abstractmethod
    def authenticate_inbound(self, payload: bytes, headers: dict[str,str]) -> InboundMessage: ...
    @abstractmethod
    def send(self, message: OutboundMessage) -> None: ...
