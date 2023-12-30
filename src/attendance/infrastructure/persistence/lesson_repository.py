from src.dto.models import GroupId
from src.repositories.impls.postgres_repository import PostgresRepositoryImpl

from ...domain.models import Lesson
from ...domain.repositories import LessonRepository
from ...domain.repositories.dto import CreateLessonDTO

__all__ = [
    "LessonRepositoryImpl",
]


class LessonRepositoryImpl(PostgresRepositoryImpl, LessonRepository):
    async def create(self, data: CreateLessonDTO) -> Lesson:
        query = "INSERT INTO lessons (name, group_id, start_time) VALUES($1, $2, $3) RETURNING id"
        lesson_id = await self._con.fetchval(query, data.name, data.group_id, data.start_time)

        return Lesson(
            id=lesson_id,
            name=data.name,
            group_id=data.group_id,
            start_time=data.start_time,
        )

    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson]:
        query = "SELECT * FROM lessons WHERE group_id = $1 ORDER BY start_time"
        records = await self._con.fetch(query, group_id)

        return [Lesson.from_mapping(record) for record in records]

    async def delete_all(self) -> None:
        query = "TRUNCATE TABLE lessons CASCADE"
        await self._con.execute(query)
