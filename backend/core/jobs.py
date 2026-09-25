from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, TypeVar

T = TypeVar("T")


class BackgroundJobRunner:
    def __init__(self, workers: int = 2) -> None:
        if not 1 <= workers <= 8: raise ValueError("workers must be between 1 and 8")
        self._executor = ThreadPoolExecutor(max_workers=workers)

    def submit(self, fn: Callable[..., T], *args: object, **kwargs: object) -> Future[T]:
        return self._executor.submit(fn, *args, **kwargs)
