from src.dto.models import (
    Group,
    GroupId,
    UniversityId
)
from src.enums import UniversityAlias
from src.repositories import GroupRepository
from src.services.interfaces import GroupService

__all__ = [
    "GroupServiceImpl",
]


class GroupServiceImpl(GroupService):
    _group_repository: GroupRepository

    def __init__(self, group_repository: GroupRepository) -> None:
        self._group_repository = group_repository

    async def find_by_name(self, name: str) -> Group | None:
        return await self._group_repository.find_by_name(name)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        return await self._group_repository.find_by_name_and_uni(name, university_alias)

    async def get_by_id(self, group_id: GroupId) -> Group:
        return await self._group_repository.get_by_id(group_id)

    async def all(self) -> list[Group]:
        return await self._group_repository.all()

    async def create_or_return(self, name: str, university_id: UniversityId) -> Group:
        found_group = await self.find_by_name(name)

        if found_group is not None:
            return found_group

        return await self._group_repository.create(name, university_id)
