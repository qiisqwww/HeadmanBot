from typing import Any, Mapping

from src.repositories.asyncpg_repository import AsyncpgRepository

from ..dto import Group

__all__ = [
    "GroupRepository",
]


class GroupRepository(AsyncpgRepository[Group]):
    async def get(self, id: int) -> Group | None:
        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, id)

        if record is None:
            return None

        return Group.from_mapping(record)

    async def all(self) -> list[Group]:
        query = "SELECT * from groups"
        records = await self._con.fetch(query)

        return [Group.from_mapping(record) for record in records]

    async def create(self, data: Mapping) -> Group:
        query = "INSERT INTO groups (name) VALUES ($1) RETURNING id"
        id = await self._con.fetchval(query, data["name"])

        return Group(
            id=id,
            name=data["name"],
        )

    async def update(self, dto: Group) -> Group:
        query = "UPDATE groups SET name=$1 WHERE id=$2"
        await self._con.execute(query, dto.name, dto.id)

        return dto

    async def patch(self, dto: Group, column: str, new_value: Any) -> Group:
        query = "UPDATE groups SET $1=$2 WHERE id=$3"
        await self._con.execute(query, column, new_value, dto.id)
        setattr(dto, column, new_value)
        return dto

    async def delete(self, dto: Group) -> None:
        query = "DELETE FROM groups WHERE id = $1"
        await self._con.execute(query, dto.id)

    async def get_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group.from_mapping(record)
