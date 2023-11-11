from typing import Any, Mapping

from src.repositories.asyncpg_repository import AsyncpgRepository

from ..dto import University

__all__ = [
    "UniversityRepository",
]


class UniversityRepository(AsyncpgRepository[University]):
    async def get(self, id: int) -> University | None:
        query = "SELECT * FROM universities WHERE id = $1"
        record = await self._con.fetchrow(query, id)

        if record is None:
            return None

        return University.from_mapping(record)

    async def all(self) -> list[University]:
        query = "SELECT * from universities"
        records = await self._con.fetch(query)

        return [University.from_mapping(record) for record in records]

    async def create(self, data: Mapping) -> University:
        query = "INSERT INTO universities (name) VALUES ($1) RETURNING id"
        id = await self._con.fetchval(query, data["name"])

        return University(
            id=id,
            name=data["name"],
        )

    async def update(self, dto: University) -> University:
        query = "UPDATE universities SET name=$1 WHERE id=$2"
        await self._con.execute(query, dto.name, dto.id)
        return dto

    async def patch(self, dto: University, column: str, new_value: Any) -> University:
        query = "UPDATE universities SET $1=$2 WHERE id=$3"
        await self._con.execute(query, column, new_value, dto.id)
        setattr(dto, column, new_value)
        return dto

    async def delete(self, dto: University) -> None:
        query = "DELETE FROM universities WHERE id = $1"
        await self._con.execute(query, dto.id)

    async def get_by_name(self, name: str) -> University | None:
        query = "SELECT id FROM universities WHERE name  = $1"
        row: Mapping | None = await self._con.fetchrow(query, name)

        if row is None:
            return None

        return University.from_mapping(row)
