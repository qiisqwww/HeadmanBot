from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.group.api.dto import GroupDTO
from src.modules.group.internal.services import GroupService
from src.modules.university.api.dto import UniversityId
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "PostgresService",
]


class GroupContract(PostgresService):
    _group_service: GroupService

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._group_service = GroupService(con)

    async def create_or_return_group(self, group_name: str, university_id: UniversityId) -> GroupDTO:
        return await self._group_service.create_or_return(group_name, university_id)

    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        return await self._group_service.find_by_name_and_uni(name, university_alias)

    async def find_by_name(self, name: str) -> GroupDTO | None:
        return await self._group_service.find_by_name(name)

    async def get_all_groups(self) -> list[GroupDTO]:
        return await self._group_service.all()
