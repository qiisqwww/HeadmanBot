from src.application.common.exceptions import CorruptedDatabaseError
from src.application.edu_info.repositories import UniversityRepository
from src.domain.edu_info import University, UniversityAlias
from src.infrastructure.common.persistence.postgres_repository import (
    PostgresRepositoryImpl,
)

__all__ = [
    "UniversityRepositoryImpl",
]


class UniversityRepositoryImpl(PostgresRepositoryImpl, UniversityRepository):
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        query = "SELECT * FROM universities WHERE alias LIKE $1"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {alias=}")

        return University.from_mapping(record)

    # async def all(self) -> list[University]:
    #     query = "SELECT * FROM universities"
    #     records = await self._con.fetch(query)
    #
    #     return [University.from_mapping(record) for record in records]

    # async def get_by_id(self, university_id: UniversityId) -> University:
    #     query = "SELECT * FROM universities WHERE id = $1"
    #     record = await self._con.fetchrow(query, university_id)
    #
    #     if record is None:
    #         raise CorruptedDatabaseError(f"Not found university with {university_id=}")
    #
    #     return University.from_mapping(record)
    #
    # async def find_by_name(self, name: str) -> None | University:
    #     query = "SELECT * FROM universities WHERE name LIKE $1"
    #     record = await self._con.fetchrow(query, name)
    #
    #     if record is None:
    #         return None
    #
    #     return University.from_mapping(record)
    #
    # async def create(self, name: str, alias: UniversityAlias) -> None:
    #     query = "INSERT INTO universities (name, alias) VALUES($1, $2)"
    #     await self._con.execute(query, name, alias)
