from ..dto.group import Group
from .base import Service

__all__ = [
    "GroupService",
]


class GroupService(Service):
    async def get(self, group_id: int) -> Group | None:
        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            return record

        return Group.from_record(record)

    async def get_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name like $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return record

        return Group.from_record(record)

    async def create(self, name: str) -> Group:
        group = await self.get_by_name(name)

        if group:
            return group

        query = "INSERT INTO groups (name) VALUES($1) RETURNING id"
        group_id: int = await self._con.fetchval(query, name)
        return Group(id=group_id, name=name)

    async def all(self) -> tuple[Group, ...]:
        query = "SELECT * FROM groups"
        records = await self._con.fetch(query)

        return tuple(Group.from_record(record) for record in records)
