from abc import ABC, abstractmethod
from typing import Any

__all__ = [
    "AsyncJob",
]


class AsyncJob(ABC):
    _trigger: str | None = None
    _trigger_args: dict[str, Any] | None = None

    @property
    def trigger(self) -> str | None:
        return self._trigger

    @property
    def trigger_args(self) -> dict[str, Any]:
        return {} if self._trigger_args is None else self._trigger_args

    @abstractmethod
    async def __call__(self) -> None:
        pass
