from dataclasses import dataclass
from threading import Lock
from uuid import UUID


@dataclass(frozen=True)
class UserSettings:
    user_id: UUID
    language: str = "id"
    theme: str = "system"
    timezone: str = "UTC"

    def __post_init__(self) -> None:
        if self.language not in {"id", "en"}:
            raise ValueError("unsupported language")
        if self.theme not in {"system", "light", "dark"}:
            raise ValueError("unsupported theme")
        if len(self.timezone) > 64 or not self.timezone.strip():
            raise ValueError("invalid timezone")


class SettingsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._items: dict[UUID, UserSettings] = {}

    def get(self, user_id: UUID) -> UserSettings:
        with self._lock:
            return self._items.get(user_id, UserSettings(user_id=user_id))

    def put(self, settings: UserSettings) -> UserSettings:
        with self._lock:
            self._items[settings.user_id] = settings
            return settings
