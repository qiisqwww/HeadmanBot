from datetime import datetime

from src.services.lesson_service import LessonService

from ..dto import Lesson, Student
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
            group = await groups_service.create(group_name)

        university_id = MIREA_ID  # TODO: Create UniversityService
        query = "INSERT INTO students (telegram_id, group_id, university_id, name, surname, telegram_name, is_headman) VALUES($1, $2, $3, $4, $5, $6, $7)"

        await self._con.execute(query, telegram_id, group.id, university_id, name, surname, telegram_name, False)

    async def make_headman(self, telegram_id: int) -> None:
        query = "UPDATE students SET is_headman = true WHERE telegram_id = $1"
        await self._con.execute(query, telegram_id)

    async def get(self, telegram_id: int) -> Student | None:
        query = "SELECT * FROM students WHERE telegram_id = $1"
        record = await self._con.fetchrow(query, telegram_id)

        if record is None:
            return None

        return Student.from_record(record)

    async def filter_by_group(self, group_id: int) -> tuple[Student, ...] | None:
        query = "SELECT * FROM students WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        if records is None:
            return None

        return tuple(Student.from_record(record) for record in records)

    async def all(self) -> tuple[Student, ...]:
        query = "SELECT * from students"
        records = await self._con.fetch(query)

        return tuple(Student.from_record(record) for record in records)

    async def get_schedule(self, student_id: int) -> tuple[Lesson, ...] | None:
        async with StudentService() as student_service:
            student = await student_service.get(student_id)

        async with GroupService() as group_service:
            group = await group_service.get(student.group_id)

        async with LessonService() as lesson_service:
            lessons = await lesson_service.get_by_group(group.id)

        lessons = tuple(filter(lambda lesson: lesson.weekday == datetime.now().weekday(), lessons))

        if lessons is None:
            return None

        return lessons
