from typing import final

from src.modules.common.infrastructure.repositories import PostgresRepositoryImpl
from src.modules.student_management.application.repositories import (
    StudentInfoRepository,
)
from src.modules.student_management.domain import StudentInfo, Role

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

    async def get_role_by_telegram_id(self, telegram_id: int) -> Role:
        query = """SELECT role FROM student_management.students WHERE telegram_id = $1"""
        record = await self._con.fetch(query, telegram_id)

        return Role(record)
