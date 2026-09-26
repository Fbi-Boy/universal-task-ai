from dataclasses import dataclass

@dataclass(frozen=True)
class HealthReport:
    status: str
    checks: tuple[str, ...]

class RuntimeHealth:
    def __init__(self, services):
        self.services = services

    def check(self):
        checks = tuple(
            name for name, value in vars(self.services).items() if value is not None
        )
        return HealthReport(
            "ok" if len(checks) == len(vars(self.services)) else "degraded",
            checks,
        )
