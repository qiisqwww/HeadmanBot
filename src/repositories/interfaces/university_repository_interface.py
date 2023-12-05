from abc import abstractmethod

from src.dto import University, UniversityId
from src.enums import UniversityAlias

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "UniversityRepository",
]


class UniversityRepository(PostgresRepository):
    @abstractmethod
    async def all(self) -> list[University]:
        ...

    @abstractmethod
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        ...

    @abstractmethod
    async def get_by_id(self, university_id: UniversityId) -> University:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> None | University:
        ...

    @abstractmethod
    async def create(self, name: str, alias: UniversityAlias) -> None:
        ...
