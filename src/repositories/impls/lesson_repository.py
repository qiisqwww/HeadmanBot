from datetime import time

from src.dto.models import GroupId, Lesson

from ..interfaces import LessonRepository
from .postgres_repository import PostgresRepositoryImpl

__all__ = [
    "LessonRepositoryImpl",
]


class LessonRepositoryImpl(PostgresRepositoryImpl, LessonRepository):
    async def create(self, name: str, group_id: GroupId, start_time: time) -> None:
        query = "INSERT INTO lessons (name, group_id, start_time) VALUES($1, $2, $3)"
        await self._con.execute(query, name, group_id, start_time)

    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson] | None:
        query = "SELECT * FROM lessons WHERE group_id = $1 ORDER BY start_time"
        records = await self._con.fetch(query, group_id)

        return [Lesson.from_mapping(record) for record in records]

    async def delete_all_lessons(self) -> None:
        query = "TRUNCATE TABLE lessons CASCADE"
        await self._con.execute(query)
