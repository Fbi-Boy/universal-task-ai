from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class RetentionPolicy:
    max_age_days: int = 30

    def cutoff(self, now: datetime | None = None) -> datetime:
        if self.max_age_days < 1:
            raise ValueError("max_age_days must be positive")
        current = now or datetime.now(timezone.utc)
        return current - timedelta(days=self.max_age_days)
