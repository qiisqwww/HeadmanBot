from src.dto import Group, Student

from .service import Service

__all__ = [
    "StudentService",
]


class StudentService(Service):
    async def register(
        self, telegram_id: int, name: str, surname: str, birthday: int | None, birthmonth: int | None
    ) -> None:
        query = "INSERT INTO students (telegram_id, name, surname, birthday, birthmonth) VALUES ($1, $2, $3, $4, $5)"
        await self._con.execute(query, telegram_id, name, surname, birthday, birthmonth)

    async def find(self, telegram_id: int) -> Student | None:
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
        query = "SELECT * FROM students_group JOIN students ON student_id = telegram_id WHERE group_id = $1"
        records = await self._con.fetch(query, group.id)

        return [Student.from_mapping(record) for record in records]
