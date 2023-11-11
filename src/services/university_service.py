from src.repositories.university_repository import UniversityRepository

from .base import Service

__all__ = [
    "UniversityService",
]


class UniversityService(Service):
    async def exists(self, name: str) -> bool:
        uni = await UniversityRepository(self._con).get_by_name(name)

        return uni is not None

    async def create(self, name: str) -> None:
        if await self.exists(name):
            return

        query = "INSERT INTO universities(name) VALUES($1)"
        await self._con.execute(query, name)
