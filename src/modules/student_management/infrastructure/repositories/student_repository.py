from datetime import date
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
        query = """SELECT id, telegram_id, first_name, last_name, role, group_id, birthdate, attendance_noted
                   FROM student_management.students
                   WHERE id = $1"""

        record = await self._con.fetchrow(query, student_id)
        return None if record is None else self._mapper.to_domain(record)

    async def find_by_telegram_id(self, telegram_id: int) -> Student | None:
        query = """SELECT id, telegram_id, first_name, last_name, role, group_id, birthdate, attendance_noted
                   FROM student_management.students
                   WHERE telegram_id = $1"""

        record = await self._con.fetchrow(query, telegram_id)
        return None if record is None else self._mapper.to_domain(record)

    async def find_by_group_id_and_role(self, group_id: int, role: Role) -> Student | None:
        query = """SELECT id, telegram_id, first_name, last_name, role, group_id, birthdate, attendance_noted
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
                   (telegram_id, group_id, first_name, last_name, role, birthdate, attendance_noted)
                   VALUES ($1, $2, $3, $4, $5, $6, $7)
                   RETURNING id"""

        student_id = await self._con.fetchval(
            query,
            student_data.telegram_id,
            group_id,
            student_data.first_name,
            student_data.last_name,
            student_data.role,
            student_data.birthdate,
            False,
        )

        return Student(
            id=student_id,
            telegram_id=student_data.telegram_id,
            group_id=group_id,
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            role=student_data.role,
            birthdate=student_data.birthdate,
            attendance_noted=False,
        )

    async def update_attendance_noted_all(self, new_attendance_noted: bool) -> None:
        query = "UPDATE student_management.students SET attendance_noted = $1"
        await self._con.execute(query, new_attendance_noted)

    async def update_attendance_noted_by_id(self, student_id: int, new_attendance_noted: bool) -> None:
        query = "UPDATE student_management.students SET attendance_noted = $1 WHERE id = $2"
        await self._con.execute(query, new_attendance_noted, student_id)

    async def update_first_name_by_id(self, student_id: int, new_first_name: str) -> None:
        query = "UPDATE student_management.students SET first_name = $1 WHERE id = $2"
        await self._con.execute(query, new_first_name, student_id)

    async def update_last_name_by_id(self, student_id: int, new_last_name: str) -> None:
        query = "UPDATE student_management.students SET last_name = $1 WHERE id = $2"
        await self._con.execute(query, new_last_name, student_id)

    async def update_birthdate_by_id(self, student_id: int, new_birthdate: date | None) -> None:
        query = "UPDATE student_management.students SET birthdate = $1 WHERE id = $2"
        await self._con.execute(query, new_birthdate, student_id)
