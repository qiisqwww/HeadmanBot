from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.group.api.contract import GroupContract
from src.modules.group.api.dto import GroupDTO

__all__ = [
    "GroupGateway",
]


class GroupGateway(PostgresService):
    _group_contract: GroupContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._group_contract = GroupContract(con)

    async def get_all_groups(self) -> list[GroupDTO]:
        return await self._group_contract.get_all_groups()
