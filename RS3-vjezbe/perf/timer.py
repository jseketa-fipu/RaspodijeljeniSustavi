import time
from types import TracebackType
from typing import Optional, Literal, Type


class Timer:
    def __init__(self, label: str) -> None:
        self.label = label
        self._start: Optional[float] = None
        self.elapsed: Optional[float] = None

    def __enter__(self) -> "Timer":
        self._start = time.perf_counter()
        return self

    # has to return Literal[False] so it doesn't suppress exceptions
    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        exception: Optional[BaseException],
        traceback_type: Optional[TracebackType],
    ) -> Literal[False]:
        self.elapsed = time.perf_counter() - (self._start or 0.0)
        print(f"{self.label} took {self.elapsed:.3f}s")
        return False  # don’t suppress exceptions
