from datetime import date
from typing import final

from src.common.repositories import PostgresRepository
from src.dto import CreateStudentDTO, StudentEnterGroupDTO
from src.dto.entities import Student, GroupId, StudentId
from src.dto.enums import Role

__all__ = [
    "StudentRepository",
]


@final
class StudentRepository(PostgresRepository):

    async def find_by_id(self, student_id: int) -> Student | None:
        query = """SELECT *
                   FROM students
                   WHERE id = $1 AND NOT archived"""

        record = await self._con.fetchrow(query, student_id)
        return None if record is None else Student.from_record(record)

    async def find_by_telegram_id(self, telegram_id: int) -> Student | None:
        query = """SELECT *
                   FROM students
                   WHERE telegram_id = $1 AND NOT archived"""

        record = await self._con.fetchrow(query, telegram_id)
        return None if record is None else Student.from_record(record)

    async def find_by_group_id_and_role(
            self,
            group_id: GroupId,
            role: Role,
    ) -> Student | None:
        query = """SELECT *
                   FROM students
                   WHERE group_id = $1 AND role = $2 AND NOT archived"""

        record = await self._con.fetchrow(query, group_id, role)
        return None if record is None else Student.from_record(record)

    async def filter_by_group_id(
            self,
            group_id: GroupId,
    ) -> Student | None:
        query = """SELECT *
                   FROM students
                   WHERE group_id = $1 AND NOT archived"""

        record = await self._con.fetchrow(query, group_id)
        return None if record is None else Student.from_record(record)

    async def find_by_fullname_and_group_id(
            self,
            last_name: str,
            first_name: str,
            group_id: int,
    ) -> Student | None:
        query = """SELECT *
                   FROM students
                   WHERE first_name = $1 AND last_name = $2 AND group_id = $3 AND NOT archived"""

        record = await self._con.fetchrow(query, first_name, last_name, group_id)
        return None if record is None else Student.from_record(record)

    async def create(
            self,
            student_data: CreateStudentDTO,
            group_id: GroupId,
    ) -> Student:
        query = """INSERT INTO students
                   (telegram_id, group_id, first_name, last_name, role, birthdate, attendance_noted, username)
                   VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
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
            student_data.username,
        )

        return Student(
            id=StudentId(student_id),
            telegram_id=student_data.telegram_id,
            group_id=group_id,
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            role=student_data.role,
            birthdate=student_data.birthdate,
            attendance_noted=False,
            username=student_data.username,
        )

    async def update_attendance_noted_all(self, new_attendance_noted: bool) -> None:
        query = "UPDATE students SET attendance_noted = $1 WHERE NOT archived"
        await self._con.execute(query, new_attendance_noted)

    async def update_attendance_noted_by_id(
            self,
            student_id: StudentId,
            new_attendance_noted: bool,
    ) -> None:
        query = "UPDATE students SET attendance_noted = $1 WHERE id = $2 AND NOT archived"
        await self._con.execute(query, new_attendance_noted, student_id)

    async def update_first_name_by_id(self, student_id: StudentId, new_first_name: str) -> None:
        query = "UPDATE students SET first_name = $1 WHERE id = $2 AND NOT archived"
        await self._con.execute(query, new_first_name, student_id)

    async def update_last_name_by_id(self, student_id: int, new_last_name: str) -> None:
        query = "UPDATE students SET last_name = $1 WHERE id = $2 AND NOT archived"
        await self._con.execute(query, new_last_name, student_id)

    async def update_birthdate_by_id(
            self,
            student_id: int,
            new_birthdate: date | None,
    ) -> None:
        query = "UPDATE students SET birthdate = $1 WHERE id = $2 AND NOT archived"
        await self._con.execute(query, new_birthdate, student_id)

    async def get_students_count(self) -> int:
        query = "SELECT COUNT(id) FROM students WHERE NOT archived"
        return await self._con.fetchval(query)

    async def get_active_students_count(self) -> int:
        query = "SELECT COUNT(id) FROM students WHERE attendance_noted = TRUE AND NOT archived"
        return await self._con.fetchval(query)

    async def delete_by_telegram_id(self, telegram_id: int) -> None:
        query = "UPDATE students SET archived=TRUE WHERE telegram_id = $1"
        await self._con.execute(query, telegram_id)

    async def delete_by_fullname_and_group_id(
            self,
            first_name: str,
            last_name: str,
            group_id: GroupId,
    ) -> None:
        query = """UPDATE students
                   SET archived=TRUE
                   WHERE first_name = $1 AND last_name = $2 AND group_id = $3"""
        await self._con.execute(query, first_name, last_name, group_id)

    async def delete_all_by_group_id(self, group_id: GroupId) -> None:
        query = "UPDATE students SET archived=TRUE WHERE group_id = $1"
        await self._con.execute(query, group_id)

    async def set_role_by_id(self, student_id: StudentId, role: Role) -> None:
        query = "UPDATE students SET role=$1 WHERE id = $2 AND NOT archived"
        await self._con.fetch(query, role.value, student_id)

    async def filter_by_group_id(self, group_id: GroupId) -> list[Student]:
        query = "SELECT * FROM students WHERE group_id = $1 AND NOT archived"
        records = await self._con.fetch(query, group_id)
        return [Student.from_record(record) for record in records]

    async def expel_user_from_group_by_id(self, student_id: StudentId) -> None:
        query = "UPDATE students SET group_id = NULL WHERE id = $1 AND NOT archived"
        await self._con.execute(query, student_id)

    async def enter_group_by_telegram_id(self, student_data: StudentEnterGroupDTO, group_id: GroupId) -> None:
        query_update = "UPDATE students SET group_id = $1, role = $2 WHERE telegram_id = $3 AND NOT archived"
        await self._con.execute(query_update, group_id, student_data.role.value, student_data.telegram_id)

    async def change_admin_group_by_telegram_id(self, telegram_id: int, group_id: GroupId) -> None:
        query = "UPDATE students SET group_id = $1 WHERE telegram_id = $2 AND NOT archived"
        await self._con.execute(query, group_id, telegram_id)
