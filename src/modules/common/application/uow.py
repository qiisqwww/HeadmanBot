from abc import abstractmethod
from types import TracebackType

from .dependency import Dependency


class UnitOfWork(Dependency):
    @abstractmethod
    async def __aenter__(self) -> None:
        ...

    @abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        ...
