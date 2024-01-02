from abc import abstractmethod

from src.domain.edu_info import Group, UniversityAlias

__all__ = [
    "GroupRepository",
]


class GroupRepository:
    @abstractmethod
    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        ...

    # @abstractmethod
    # async def find_by_name(self, name: str) -> Group | None:
    #     ...
    #
    # @abstractmethod
    # async def get_by_id(self, group_id: GroupId) -> Group:
    #     ...
    #
    # @abstractmethod
    # async def all(self) -> list[Group]:
    #     ...
    #
    # @abstractmethod
    # async def create(self, name: str, university_id: UniversityId) -> Group:
    #     ...
