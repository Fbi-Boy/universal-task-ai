from dataclasses import dataclass


@dataclass
class IdempotencyStore:
    _results: dict[str, object]

    def __init__(self) -> None:
        self._results = {}

    def get(self, key: str) -> object | None:
        return self._results.get(key)

    def put_once(self, key: str, result: object) -> bool:
        if key in self._results:
            return False
        self._results[key] = result
        return True
