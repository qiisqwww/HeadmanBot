from datetime import date

from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentId

__all__ = [
    "BirthdateService",
]


class BirthdateService(PostgresService):
    async def get_by_student_id(self, student_id: StudentId) -> date | None:
        query = "SELECT birthdate FROM birthdates.birthdates WHERE student_id = $1"

        return await self._con.fetchval(query, student_id)

    async def create(self, student_id: StudentId, birthdate: date | None) -> None:
        query = "INSERT INTO birthdates.birthdates (student_id, birthdate) VALUES ($1, $2)"

        await self._con.execute(query, student_id, birthdate)
