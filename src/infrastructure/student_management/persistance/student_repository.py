from src.dto.models import (
    GroupId,
    Student,
    StudentId,
    StudentLoginData
)
from src.enums import Role

from ..interfaces import StudentRepository
from .postgres_repository import PostgresRepositoryImpl

__all__ = [
    "StudentRepositoryImpl",
]


class StudentRepositoryImpl(PostgresRepositoryImpl, StudentRepository):
    async def create_and_return(
        self,
        student_raw: StudentLoginData,
        group_id: GroupId,
    ) -> Student:
        query = (
            "INSERT INTO students "
            "(telegram_id, group_id, name, surname, role, birthdate) "
            "VALUES ($1, $2, $3, $4, $5, $6)"
        )
        await self._con.execute(
            query,
            student_raw.telegram_id,
            group_id,
            student_raw.name,
            student_raw.surname,
            student_raw.role,
            student_raw.birthdate,
        )

        return Student(
            telegram_id=StudentId(student_raw.telegram_id),
            group_id=group_id,
            name=student_raw.name,
            surname=student_raw.surname,
            role=student_raw.role,
            birthdate=student_raw.birthdate,
        )

    async def find_by_id(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def find_by_group_id_and_role(self, group_id: GroupId, role: Role) -> Student | None:
        query = "SELECT * FROM students WHERE group_id = $1 AND role LIKE $2"
        record = await self._con.fetchrow(query, group_id, role)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def all(self) -> list[Student]:
        query = "SELECT * FROM students"
        records = await self._con.fetch(query)

        return [Student.from_mapping(record) for record in records]

    async def filter_group_by_id(self, group_id: GroupId) -> list[Student] | None:
        query = "SELECT * FROM students WHERE group_id = $1"

        records = await self._con.fetch(query, group_id)
        return [Student.from_mapping(record) for record in records]

    async def update_surname_by_id(self, new_surname: str, student_id: StudentId) -> None:
        query = ("UPDATE students "
                 "SET surname = $1 "
                 "WHERE telegram_id = $2")

        await self._con.execute(query, new_surname, student_id)

    async def update_name_by_id(self, new_name: str, student_id: StudentId) -> None:
        query = ("UPDATE students "
                 "SET name = $1 "
                 "WHERE telegram_id = $2")

        await self._con.execute(query, new_name, student_id)