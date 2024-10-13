from datetime import UTC, time
from typing import final

from src.modules.attendance.domain import Lesson
from src.modules.utils.schedule_api.domain import Schedule

__all__ = [
    "LessonRepository",
]


@final
class LessonRepository(PostgresRepository):
    async def filter_by_group_id(self, group_id: int) -> list[Lesson]:
        query = "SELECT * FROM lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        return [Lesson(**record) for record in records]

    async def create_for_group(self, group_id: int, schedule: list[Schedule]) -> list[Lesson]:
        query = "INSERT INTO lessons (name, group_id, start_time) VALUES($1, $2, $3) RETURNING id"
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

    async def delete_lessons_by_group_id(self, group_id: int) -> None:
        query = "DELETE FROM lessons WHERE group_id = $1"
        await self._con.execute(query, group_id)
