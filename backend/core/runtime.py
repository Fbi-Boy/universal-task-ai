from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimeServices:
    """Explicit dependency container for runtime composition."""
    task_dispatcher: object
    notification_dispatcher: object
    approval_flow: object
    research_provider: object

class RuntimeComposition:
    def __init__(self, services: RuntimeServices):
        self.services = services

    def validate(self):
        missing = [
            name for name, value in vars(self.services).items()
            if value is None
        ]
        if missing:
            raise ValueError("missing runtime services: " + ",".join(missing))
        return self.services
