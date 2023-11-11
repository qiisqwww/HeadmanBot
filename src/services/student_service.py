from src.dto.student import Student

from .base import Service
from .group_service import GroupService

__all__ = [
    "StudentService",
]

MIREA_ID = 1


class StudentService(Service):
    async def create(
        self, telegram_id: int, name: str, surname: str, telegram_name: str | None, group_name: str
    ) -> None:
        groups_service = GroupService(self._con)
        group = await groups_service.create(group_name)

        university_id = MIREA_ID  # TODO: Create UniversityService
        query = (
            "INSERT INTO students (telegram_id, group_id, university_id, name, surname, telegram_name, is_headman)"
            "VALUES($1, $2, $3, $4, $5, $6, $7)"
        )

        await self._con.execute(query, telegram_id, group.id, university_id, name, surname, telegram_name, False)

    async def make_headman(self, student: Student) -> None:
        query = "UPDATE students SET is_headman = true WHERE telegram_id = $1"
        await self._con.execute(query, student.telegram_id)
