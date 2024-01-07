from src.modules.common.application.exceptions import CorruptedDatabaseError
from src.modules.common.domain import UniversityAlias
from src.modules.common.infrastructure.persistence.postgres_repository import (
    PostgresRepositoryImpl,
)
from src.modules.edu_info.application.repositories import UniversityRepository
from src.modules.edu_info.domain import University

__all__ = [
    "UniversityRepositoryImpl",
]


class UniversityRepositoryImpl(PostgresRepositoryImpl, UniversityRepository):
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        query = "SELECT * FROM universities WHERE alias = $1"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {alias=}")

        return University(
            id=record["id"],
            name=record["name"],
            alias=UniversityAlias(record["alias"]),
        )

    async def all(self) -> list[University]:
        query = "SELECT * FROM universities"
        records = await self._con.fetch(query)

        return [
            University(
                id=record["id"],
                name=record["name"],
                alias=UniversityAlias(record["alias"]),
            )
            for record in records
        ]

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
