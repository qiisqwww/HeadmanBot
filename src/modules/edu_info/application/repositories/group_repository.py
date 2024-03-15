from abc import ABC, abstractmethod

from src.modules.common.domain import UniversityAlias

from ...domain import Group

__all__ = [
    "GroupRepository",
]


class GroupRepository(ABC):
    @abstractmethod
    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> Group | None:
        ...

    @abstractmethod
    async def create(self, name: str, university_id: int) -> Group:
        ...

    @abstractmethod
    async def find_by_id(self, group_id: int) -> Group | None:
        ...

    @abstractmethod
    async def all(self) -> list[Group]:
        ...

    @abstractmethod
    async def delete_by_id(self, group_id: int) -> None:
        ...
