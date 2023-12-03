from src.kernel.base import PostgresService
from src.kernel.external.database import CorruptedDatabaseError
from src.modules.university.api.dto import UniversityDTO, UniversityId
from src.modules.university.api.enums import UniversityAlias
from src.modules.university.internal.config import UNIVERSITIES_LIST

__all__ = [
    "UniversityService",
]


class UniversityService(PostgresService):
    async def add_universities(self) -> None:
        for name, alias in UNIVERSITIES_LIST:
            await self._try_create(name, alias)

    async def all(self) -> list[UniversityDTO]:
        query = "SELECT * FROM universities.universities"
        records = await self._con.fetch(query)

        return [UniversityDTO.from_mapping(record) for record in records]

    async def get_by_alias(self, alias: UniversityAlias) -> UniversityDTO:
        query = "SELECT * FROM universities.universities WHERE alias LIKE $1"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {alias=}")

        return UniversityDTO.from_mapping(record)

    async def get_by_id(self, university_id: UniversityId) -> UniversityDTO:
        query = "SELECT * FROM universities.universities WHERE id = $1"
        record = await self._con.fetchrow(query, university_id)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {university_id=}")

        return UniversityDTO.from_mapping(record)

    async def _find_by_name(self, name: str) -> None | UniversityDTO:
        query = "SELECT * FROM universities.universities WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return UniversityDTO.from_mapping(record)

    async def _try_create(self, name: str, alias: UniversityAlias) -> None:
        """Trying create new universities.university if is does not exists."""

        found_university = await self._find_by_name(name)

        if found_university is not None:
            return

        query = "INSERT INTO universities.universities (name, alias) VALUES($1, $2)"
        await self._con.execute(query, name, alias)
