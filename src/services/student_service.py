from src.dto import Group, Student

from .group_service import GroupService
from .service import Service

__all__ = [
    "StudentService",
]


class StudentService(Service):
    async def register(
        self, telegram_id: int, name: str, surname: str, university_id: int, group_name: str, is_headman: bool
    ) -> None:
        group_service = GroupService(self._con)
        student_group = await group_service.try_create_or_return(group_name)

        query = (
            "INSERT INTO students "
            "(telegram_id, group_id, university_id, name, surname, is_headman)"
            " VALUES ($1, $2, $3, $4, $5, $6)"
        )

        await self._con.execute(query, telegram_id, student_group.id, university_id, name, surname, is_headman)

    async def find(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_mapping(record)

    async def make_headman(self, student: Student) -> None:
        query = "UPDATE students SET is_headman=true WHERE telegram_id=$1"
        await self._con.execute(query, student.telegram_id)

        student.is_headman = True

    async def all(self) -> list[Student]:
        query = "SELECT * FROM students"
        records = await self._con.fetch(query)

        return [Student.from_mapping(record) for record in records]

    async def filter_by_group(self, group: Group) -> list[Student]:
        query = "SELECT * FROM students WHERE group_id = $1"
        records = await self._con.fetch(query, group.id)

        return [Student.from_mapping(record) for record in records]
