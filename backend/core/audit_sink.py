from abc import ABC, abstractmethod

from backend.core.audit import AuditEvent


class AuditSink(ABC):
    """Minimal append-only boundary for security-relevant runtime events."""

    @abstractmethod
    def append(self, event: AuditEvent) -> None:
        raise NotImplementedError


class InMemoryAuditSink(AuditSink):
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(
            event.model_copy(update={"metadata": event.safe_metadata()})
        )
