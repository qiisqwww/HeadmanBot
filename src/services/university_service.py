from ..dto import University
from .base import Service

__all__ = [
    "UniversityService",
]


class UniversityService(Service):
    async def all(self) -> list[University]:
        query = "SELECT * FROM universities"
        records = await self._con.fetch(query)

        return [University.from_record(record) for record in records]

    async def exists(self, name: str) -> bool:
        query = "SELECT id FROM universities WHERE name  = $1"
        result = await self._con.fetchval(query, name)

        return bool(result)

    async def create(self, name: str) -> None:
        if await self.exists(name):
            return None

        query = "INSERT INTO universities(name) VALUES($1)"
        await self._con.execute(query, name)
