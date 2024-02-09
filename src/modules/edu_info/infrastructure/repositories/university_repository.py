from typing import final

from src.modules.common.application.exceptions import CorruptedDatabaseError
from src.modules.common.domain import UniversityAlias
from src.modules.common.infrastructure.repositories import PostgresRepositoryImpl
from src.modules.edu_info.application.repositories import UniversityRepository
from src.modules.edu_info.domain import University
from src.modules.edu_info.infrastructure.mappers import UniversityMapper

__all__ = [
    "UniversityRepositoryImpl",
]


@final
class UniversityRepositoryImpl(PostgresRepositoryImpl, UniversityRepository):
    _mapper: UniversityMapper = UniversityMapper()

    async def get_by_alias(self, alias: UniversityAlias) -> University:
        query = "SELECT * FROM edu_info.universities WHERE alias = $1"
        record = await self._con.fetchrow(query, alias)

        if record is None:
            raise CorruptedDatabaseError(f"Not found university with {alias=}")

        return self._mapper.to_domain(record)

    async def all(self) -> list[University]:
        query = "SELECT * FROM edu_info.universities"
        records = await self._con.fetch(query)

        return [self._mapper.to_domain(record) for record in records]

    async def find_by_name(self, name: str) -> None | University:
        query = "SELECT * FROM edu_info.universities WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return self._mapper.to_domain(record)

    async def fetch_university_timezone_by_group_id(self, group_id: int) -> str:
        query = """
                SELECT uni.timezone
                FROM edu_info.universities AS uni
                JOIN edu_info.groups AS gr
                ON uni.id = gr.university_id
                WHERE gr.id = $1
        """

        value: str = await self._con.fetchval(query, group_id)
        return value
