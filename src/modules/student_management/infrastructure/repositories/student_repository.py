from typing import final

from src.modules.common.infrastructure.repositories import PostgresRepositoryImpl
from src.modules.student_management.application.repositories import (
    CreateStudentDTO,
    StudentRepository,
)
from src.modules.student_management.domain import Role, Student
from src.modules.student_management.infrastructure.mappers import StudentMapper

__all__ = [
    "StudentRepositoryImpl",
]


@final
class StudentRepositoryImpl(PostgresRepositoryImpl, StudentRepository):
    _mapper: StudentMapper = StudentMapper()

    async def find_by_id(self, student_id: int) -> Student | None:
        query = """SELECT id, telegram_id, name, surname, role, group_id, birthdate, is_checked_in_today
                   FROM student_management.students
                   WHERE id = $1"""

        record = await self._con.fetchrow(query, student_id)
        return None if record is None else self._mapper.to_domain(record)

    async def find_by_telegram_id(self, telegram_id: int) -> Student | None:
        query = """SELECT id, telegram_id, name, surname, role, group_id, birthdate, is_checked_in_today
                   FROM student_management.students
                   WHERE telegram_id = $1"""

        record = await self._con.fetchrow(query, telegram_id)
        return None if record is None else self._mapper.to_domain(record)

    async def find_by_group_id_and_role(self, group_id: int, role: Role) -> Student | None:
        query = """SELECT id, telegram_id, name, surname, role, group_id, birthdate, is_checked_in_today
                   FROM student_management.students
                   WHERE group_id = $1 AND role = $2"""

        record = await self._con.fetchrow(query, group_id, role)
        return None if record is None else self._mapper.to_domain(record)

    async def create(
        self,
        student_data: CreateStudentDTO,
        group_id: int,
    ) -> Student:
        query = """INSERT INTO student_management.students
                   (telegram_id, group_id, name, surname, role, birthdate, is_checked_in_today)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)
                   RETURNING id"""

        student_id = await self._con.fetchval(
            query,
            student_data.telegram_id,
            group_id,
            student_data.name,
            student_data.surname,
            student_data.role,
            student_data.birthdate,
            False,
        )

        return Student(
            id=student_id,
            telegram_id=student_data.telegram_id,
            group_id=group_id,
            name=student_data.name,
            surname=student_data.surname,
            role=student_data.role,
            birthdate=student_data.birthdate,
            is_checked_in_today=False,
        )

    async def update_is_checked_in(self, student_id: int, new_is_checked_in: bool) -> None:
        query = "UPDATE student_management.students SET is_checked_in_today = $1 WHERE id = $2"
        await self._con.execute(query, new_is_checked_in, student_id)

    async def update_is_checked_in_all(self, new_is_checked_in: bool) -> None:
        query = "UPDATE student_management.students SET is_checked_in_today = $1"
        await self._con.execute(query, new_is_checked_in)

    async def update_name_by_id(self, student_id: int, new_name: str) -> None:
        query = "UPDATE student_management.students SET name = $1 WHERE id = $2"
        await self._con.execute(query, new_name, student_id)

    async def update_surname_by_id(self, student_id: int, new_surname: str) -> None:
        query = "UPDATE student_management.students SET surname = $1 WHERE id = $2"
        await self._con.execute(query, new_surname, student_id)
