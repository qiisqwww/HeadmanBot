from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.university.api.dto import UniversityDTO, UniversityId
from src.modules.university.api.enums import UniversityAlias
from src.modules.university.internal.services import UniversityService

__all__ = [
    "UniversityService",
]


class UniversityContract(PostgresService):
    _university_service: UniversityService

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_service = UniversityService(con)

    async def get_university_by_alias(self, alias: UniversityAlias) -> UniversityDTO:
        return await self._university_service.get_by_alias(alias)

    async def get_university_by_id(self, university_id: UniversityId) -> UniversityDTO:
        return await self._university_service.get_by_id(university_id)

    async def get_all_universities(self) -> list[UniversityDTO]:
        return await self._university_service.all()

    async def add_universities(self) -> None:
        return await self._university_service.add_universities()
