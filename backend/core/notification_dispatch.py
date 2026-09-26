from dataclasses import dataclass
from backend.core.notification_events import NotificationEvent, NotificationKind

@dataclass(frozen=True)
class NotificationRoute:
    kind: NotificationKind
    adapter: object

class SafeNotificationDispatcher:
    """Routes only explicitly supported notification kinds to injected adapters."""
    def __init__(self, routes):
        self._routes = tuple(routes)

    def dispatch(self, event: NotificationEvent):
        if not event.run_id or not event.user_id:
            raise ValueError("notification identity is required")
        if len(event.message) > 4096:
            raise ValueError("message too large")
        delivered = 0
        for route in self._routes:
            if route.kind is event.kind:
                route.adapter.send(event)
                delivered += 1
        if delivered == 0:
            raise LookupError("no notification route configured")
        return delivered
