from datetime import time, timezone

from ..dto import Lesson
from .base import Service

__all__ = [
    "LessonService",
]


class LessonService(Service):
    async def get(self, lesson_id: int) -> Lesson | None:
        query = "SELECT * FROM lessons WHERE id = $1"
        record = await self._con.fetchrow(query, lesson_id)

        if record is None:
            return record

        return Lesson.from_record(record)

    async def get_by_group(self, group_id: int) -> tuple[Lesson, ...] | None:
        query = "SELECT * FROM lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        if records is None:
            return None

        return tuple(Lesson.from_record(record) for record in records)

    async def create(self, discipline: str, group_id: int, start_time: time, weekday: int) -> None:
        start_time = time(hour=start_time.hour, minute=start_time.minute, tzinfo=timezone.utc)
        query = "SELECT * from lessons WHERE discipline = $1 AND group_id = $2 AND start_time = $3 AND weekday = $4"

        record = await self._con.fetchrow(query, discipline, group_id, start_time, weekday)

        if record is not None:
            return

        query = "INSERT INTO lessons (discipline, group_id, start_time, weekday) VALUES($1, $2, $3, $4)"
        await self._con.execute(query, discipline, group_id, start_time, weekday)

    async def delete_all_lessons(self) -> None:
        query = "TRUNCATE TABLE lessons CASCADE"
        await self._con.execute(query)
