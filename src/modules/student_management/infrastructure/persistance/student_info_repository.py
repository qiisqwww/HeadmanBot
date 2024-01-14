from typing import final

from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl
from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
)
from src.modules.student_management.domain import StudentInfo

__all__ = [
    "StudentInfoRepositoryImpl",
]


@final
class StudentInfoRepositoryImpl(PostgresRepositoryImpl, StudentInfoRepository):
    async def filter_by_group_id(self, group_id: int) -> list[StudentInfo]:
        query = """SELECT id, telegram_id, name, surname, is_checked_in_today
                   FROM student_management.students 
                   WHERE group_id = $1"""
        records = await self._con.fetch(query, group_id)

        return [StudentInfo(**record) for record in records]
