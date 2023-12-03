from datetime import date

from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentId
from src.modules.birthdate.internal.services import BirthdateService

__all__ = [
    "BirthdateContract",
]


class BirthdateContract(PostgresService):
    _birthdate_service: BirthdateService

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._birthdate_service = BirthdateService(con)

    async def create(self, student_id: StudentId, birthdate: date | None) -> None:
        await self._birthdate_service.create(student_id, birthdate)
