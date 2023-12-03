from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.university.api import UniversityContract
from src.modules.university.api.dto import UniversityDTO
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "UniversityGatewate",
]


class UniversityGatewate(PostgresService):
    _university_contract: UniversityContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_contract = UniversityContract(con)

    async def get_university_by_alias(self, alias: UniversityAlias) -> UniversityDTO:
        return await self._university_contract.get_university_by_alias(alias)

    async def get_all_universities(self) -> list[UniversityDTO]:
        return await self._university_contract.get_all_universities()
