from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryItem:
    key: str
    value: str


class MemoryStore:
    def __init__(self) -> None:
        self._items: dict[str, MemoryItem] = {}

    def put(self, key: str, value: str) -> None:
        if not key.strip(): raise ValueError("key must not be empty")
        self._items[key] = MemoryItem(key, value)

    def get(self, key: str) -> MemoryItem | None:
        return self._items.get(key)

    def delete(self, key: str) -> None:
        self._items.pop(key, None)
