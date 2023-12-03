from datetime import date

from asyncpg.pool import PoolConnectionProxy

from src.kernel.base.postgres_service import PostgresService
from src.kernel.student_dto import StudentId
from src.modules.birthdate.api.contract import BirthdateContract

__all__ = [
    "BirthdateGateway",
]


class BirthdateGateway(PostgresService):
    _birthdate_contract: BirthdateContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._birthdate_contract = BirthdateContract(con)

    async def create_birthdate(self, student_id: StudentId, birthdate: date | None) -> None:
        await self._birthdate_contract.create(student_id, birthdate)
