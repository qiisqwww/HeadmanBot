from src.common.services import Service
from src.dto import Group, Student

from .group_service import GroupService

__all__ = [
    "StudentService",
]


class StudentService(Service):
    async def create(
        self, telegram_id: int, name: str, surname: str, birthday: int | None, birthmonth: int | None
    ) -> Student:
        query = "INSERT INTO students (telegram_id, name, surname, birthday, birthmonth) VALUES ($1, $2, $3, $4, $5)"
        await self._con.execute(query, telegram_id, name, surname, birthday, birthmonth)

        return Student(
            telegram_id=telegram_id,
            name=name,
            surname=surname,
            birthday=birthday,
            birthmonth=birthmonth,
        )

    async def find_student(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def all(self) -> list[Student]:
        query = "SELECT * FROM students"
        records = await self._con.fetch(query)

        return [Student.from_mapping(record) for record in records]

    async def filter_by_group(self, group: Group) -> list[Student]:
        query = "SELECT * FROM students_groups JOIN students ON student_id = telegram_id WHERE group_id = $1"
        records = await self._con.fetch(query, group.id)

        return [Student.from_mapping(record) for record in records]

    async def is_headman(self, student: Student) -> bool:
        group_service = GroupService(self._con)
        student_group = await group_service.get_by_student(student)

        return student_group.headman_id == student.telegram_id
