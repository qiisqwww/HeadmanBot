from src.config.config import UNIVERSITIES_LIST
from src.dto import University
from src.enums import UniversityAlias
from src.shared.services import CorruptedDatabaseError, PostgresService

__all__ = [
    "UniversityService",
]


class UniversityService(PostgresService):
    async def add_universities(self) -> None:
        for name, alias in UNIVERSITIES_LIST:
            await self._try_create(name, alias)

    async def all(self) -> list[University]:
        query = "SELECT * FROM universities.universities"
        records = await self._con.fetch(query)

        return [University.from_mapping(record) for record in records]

    async def find_by_alias(self, alias: UniversityAlias) -> University:
        query = "SELECT * FROM universities.universities WHERE alias LIKE $1"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {alias=}")

        return University.from_mapping(record)

    async def _find_by_name(self, name: str) -> University | None:
        query = "SELECT * FROM universities.universities WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return University.from_mapping(record)

    async def _create(self, name: str, alias: UniversityAlias) -> None:
        query = "INSERT INTO universities.universities (name, alias) VALUES($1, $2)"
        await self._con.execute(query, name, alias)

    async def _try_create(self, name: str, alias: UniversityAlias) -> None:
        """Trying create new universities.university if is does not exists."""
        found_university = await self._find_by_name(name)

        if found_university:
            return

        await self._create(name, alias)
