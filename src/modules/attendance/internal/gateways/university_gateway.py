from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.modules.university.api.contract import UniversityContract
from src.modules.university.api.dto import UniversityDTO, UniversityId

__all__ = [
    "UniversityGateway",
]


class UniversityGateway(PostgresService):
    _university_contract: UniversityContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_contract = UniversityContract(con)

    async def get_university_by_id(self, university_id: UniversityId) -> UniversityDTO:
        return await self._university_contract.get_university_by_id(university_id)
