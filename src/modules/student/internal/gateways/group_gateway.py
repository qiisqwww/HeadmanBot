from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.group.api import GroupContract
from src.modules.group.api.dto import GroupDTO
from src.modules.university.api.dto import UniversityId
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "GroupGateway",
]


class GroupGateway(PostgresService):
    _group_contract: GroupContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._group_contract = GroupContract(con)

    async def create_or_return_group(self, group_name: str, university_id: UniversityId) -> GroupDTO:
        return await self._group_contract.create_or_return_group(group_name, university_id)

    async def find_group_by_name_and_uni(self, group_name: str, university_alias: UniversityAlias) -> GroupDTO | None:
        return await self._group_contract.find_by_name_and_uni(group_name, university_alias)

    async def find_group_by_name(self, group_name: str) -> GroupDTO | None:
        return await self._group_contract.find_by_name(group_name)
