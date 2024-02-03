from datetime import UTC, time
from typing import final

from src.modules.attendance.application.repositories import LessonRepository
from src.modules.attendance.domain import Lesson
from src.modules.common.application.schedule_api import Schedule
from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl

__all__ = [
    "LessonRepositoryImpl",
]


@final
class LessonRepositoryImpl(PostgresRepositoryImpl, LessonRepository):
    async def filter_by_group_id(self, group_id: int) -> list[Lesson]:
        query = "SELECT * FROM attendance.lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        return [Lesson(**record) for record in records]

    async def create_for_group(self, group_id: int, schedule: list[Schedule]) -> list[Lesson]:
        query = "INSERT INTO attendance.lessons (name, group_id, start_time) VALUES($1, $2, $3) RETURNING id"
        lessons: list[Lesson] = []

        for lesson in schedule:
            start_time = self._create_time_with_timezone(lesson.start_time)
            lesson_id = await self._con.fetchval(query, lesson.lesson_name, group_id, start_time)
            lessons.append(
                Lesson(
                    id=lesson_id,
                    name=lesson.lesson_name,
                    group_id=group_id,
                    start_time=start_time,
                ),
            )

        return lessons

    @staticmethod
    def _create_time_with_timezone(time_without_tz: time) -> time:
        return time(hour=time_without_tz.hour, minute=time_without_tz.minute, tzinfo=UTC)

    async def delete_all(self) -> None:
        query = "TRUNCATE TABLE attendance.lessons CASCADE"
        await self._con.execute(query)
