from abc import ABC, abstractmethod
from types import TracebackType

__all__ = [
    "UnitOfWork",
]


class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self) -> None:
        ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...
