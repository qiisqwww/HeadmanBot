from typing import final

from src.common.exceptions import DatabaseCorruptedError
from src.common.repositories import PostgresRepository
from src.dto.entities import University, GroupId
from src.dto.enums import UniversityAlias

__all__ = [
    "UniversityRepositoryImpl",
]


@final
class UniversityRepository(PostgresRepository):
    async def get_by_alias(self, alias: UniversityAlias) -> University:
        query = "SELECT * FROM universities WHERE alias = $1 AND NOT archived"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            msg = f"Not found university with {alias=}"
            raise DatabaseCorruptedError(msg)

        return University.from_record(record)

    async def all(self) -> list[University]:
        query = "SELECT * FROM universities WHERE NOT archived"
        records = await self._con.fetch(query)

        return [University.from_record(record) for record in records]

    async def find_by_name(self, name: str) -> None | University:
        query = "SELECT * FROM universities WHERE name LIKE $1 AND NOT archived"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return University.from_record(record)

    async def fetch_university_timezone_by_group_id(self, group_id: GroupId) -> str:
        query = """
                SELECT uni.timezone
                FROM universities AS uni
                JOIN groups AS gr
                ON uni.id = gr.university_id
                WHERE gr.id = $1 AND NOT uni.archived AND NOT gr.archived
        """

        value: str = await self._con.fetchval(query, group_id)
        return value

    async def fetch_uni_alias_by_group_id(self, group_id: GroupId) -> UniversityAlias:
        query = """
                SELECT uni.alias
                FROM universities AS uni
                JOIN groups AS gr
                ON uni.id = gr.university_id
                WHERE gr.id = $1 AND NOT uni.archived AND NOT gr.archived
        """

        value: str = await self._con.fetchval(query, group_id)
        return UniversityAlias(value)
