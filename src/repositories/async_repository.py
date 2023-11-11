from abc import ABC, abstractmethod
from typing import Any, Generic, Mapping, TypeVar

DTO = TypeVar("DTO")

__all__ = [
    "AsyncRepository",
]


class AsyncRepository(ABC, Generic[DTO]):
    @abstractmethod
    async def get(self, id: int) -> DTO | None:
        ...

    @abstractmethod
    async def all(self) -> list[DTO]:
        ...

    @abstractmethod
    async def create(self, data: Mapping) -> DTO:
        ...

    @abstractmethod
    async def update(self, dto: DTO) -> DTO:
        ...

    @abstractmethod
    async def patch(self, dto: DTO, column: str, new_value: Any) -> DTO:
        ...

    @abstractmethod
    async def delete(self, dto: DTO) -> None:
        ...
