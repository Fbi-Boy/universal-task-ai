from backend.core.notification_dispatch import SafeNotificationDispatcher

class RuntimeNotificationService:
    def __init__(self, routes):
        self.dispatcher = SafeNotificationDispatcher(routes)

    def publish(self, event):
        return self.dispatcher.dispatch(event)
