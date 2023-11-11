from ..dto import Group
from ..repositories import GroupRepository
from .base import Service

__all__ = [
    "GroupService",
]


class GroupService(Service):
    async def create(self, name: str) -> Group:
        group = await GroupRepository(self._con).get_by_name(name)

        if group:
            return group

        query = "INSERT INTO groups (name) VALUES($1) RETURNING id"
        group_id: int = await self._con.fetchval(query, name)

        return Group(
            id=group_id,
            name=name,
        )
