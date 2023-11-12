from src.dto import University

from .service import Service

__all__ = [
    "UniversityService",
]


class UniversityService(Service):
    async def try_create(self, name: str) -> None:
        """Trying create new university if is does not exists."""
        university = await self.find_by_name(name)

        if university:
            return

        await self._create(name)

    async def find_by_name(self, name: str) -> University | None:
        query = "SELECT id FROM universities WHERE name LIKE $1"
        pk = await self._con.fetchval(query, name)

        if pk is None:
            return None

        return University(
            id=pk,
            name=name,
        )

    async def _create(self, name: str) -> None:
        query = "INSERT INTO universities (name) VALUES($1)"
        await self._con.execute(query, name)
