from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias

from ...domain import University

__all__ = [
    "UniversityRepository",
]


class UniversityRepository(ABC):
    @abstractmethod
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        ...

    @abstractmethod
    async def all(self) -> list[University]:
        ...

    @abstractmethod
    async def create(self, name: str, alias: UniversityAlias) -> None:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> None | University:
        ...
