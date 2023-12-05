from abc import abstractmethod

from src.dto import Group, GroupId, UniversityId
from src.enums import UniversityAlias
from src.repositories import GroupRepository

from .service import Service

__all__ = [
    "GroupService",
]


class GroupService(Service):
    @abstractmethod
    def __init__(self, group_repository: GroupRepository) -> None:
        ...

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
    async def create_or_return(self, name: str, university_id: UniversityId) -> Group:
        ...
