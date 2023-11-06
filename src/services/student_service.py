from ..dto.student import Student
from .base import Service
from .group_service import GroupService

__all__ = [
    "StudentService",
]

MIREA_ID = 1


class StudentService(Service):
    async def is_registered(self, telegram_id: int) -> bool:
        query = "SELECT telegram_id FROM students WHERE telegram_id = $1"
        return await self._con.fetchval(query, telegram_id) is not None

    async def is_headman(self, telegram_id: int) -> bool:
        query = "SELECT is_headman FROM students WHERE telegram_id = $1"
        return bool(await self._con.fetchval(query, telegram_id))

    async def create(
        self, telegram_id: int, name: str, surname: str, telegram_name: str | None, group_name: str
    ) -> None:
        async with GroupService() as groups_service:
            group_id = await groups_service.create(group_name)

        university_id = MIREA_ID  # TODO: Create UniversityService
        query = "INSERT INTO students VALUES($1, $2, $3, $4, $5, $6, $7)"

        await self._con.execute(query, telegram_id, group_id, university_id, name, surname, telegram_name, False)

    async def make_headman(self, telegram_id: int) -> None:
        query = "UPDATE students SET is_headman = true WHERE telegram_id = $1"
        await self._con.execute(query, telegram_id)

    async def get(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_record(record)

    async def get_by_group(self, group_name: str) -> Student | None:
        async with GroupService() as groups_service:
            group = await groups_service.get_by_name(group_name)

        if group is None:
            return None

        query = "SELECT * FROM students WHERE group_id = $1"
        record = await self._con.fetchrow(query, group.id)

        if record is None:
            return None

        return Student.from_record(record)

    async def all(self) -> tuple[Student, ...]:
        query = "SELECT * from students"
        records = await self._con.fetch(query)

        return tuple(Student.from_record(record) for record in records)
