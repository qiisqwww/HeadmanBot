from abc import abstractmethod

from src.dto import Group, GroupId, UniversityId
from src.enums import UniversityAlias

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "GroupRepository",
]


class GroupRepository(PostgresRepository):
    @abstractmethod
    async def find_by_name(self, name: str) -> Group | None:
        ...

    @abstractmethod
    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        ...

    @abstractmethod
    async def get_by_id(self, group_id: GroupId) -> Group:
        ...

    @abstractmethod
    async def all(self) -> list[Group]:
        ...

    @abstractmethod
    async def create(self, name: str, university_id: UniversityId) -> Group:
        ...
