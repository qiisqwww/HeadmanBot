from typing import Any, Mapping

from src.repositories.asyncpg_repository import AsyncpgRepository

from ..dto import Lesson

__all__ = [
    "LessonRepository",
]


class LessonRepository(AsyncpgRepository[Lesson]):
    async def get(self, id: int) -> Lesson | None:
        query = "SELECT * FROM lessons WHERE id = $1"
        record = await self._con.fetchrow(query, id)

        if record is None:
            return None

        return Lesson.from_mapping(record)

    async def all(self) -> list[Lesson]:
        query = "SELECT * from lessons"
        records = await self._con.fetch(query)

        return [Lesson.from_mapping(record) for record in records]

    async def create(self, data: Mapping) -> Lesson:
        query = "INSERT INTO lessons (discipline, group_id, start_time, weekday) VALUES ($1, $2, $3, $4) RETURNING id"
        id = await self._con.fetchval(query, data["discipline"], data["group_id"], data["start_time"], data["weekday"])

        return Lesson(
            id=id,
            discipline=data["discipline"],
            group_id=data["group_id"],
            start_time=data["start_time"],
            weekday=data["weekday"],
        )

    async def update(self, dto: Lesson) -> Lesson:
        query = "UPDATE SET discipline=$1, group_id=$2, start_time=$3, weekday=$4 WHERE id=$5"
        await self._con.execute(query, dto.discipline, dto.group_id, dto.start_time, dto.weekday, dto.id)
        return dto

    async def patch(self, dto: Lesson, column: str, new_value: Any) -> Lesson:
        query = "UPDATE lessons SET $1=$2 WHERE id=$3"
        await self._con.execute(query, column, new_value, dto.id)
        setattr(dto, column, new_value)
        return dto

    async def delete(self, dto: Lesson) -> None:
        query = "DELETE FROM lessons WHERE id = $1"
        await self._con.execute(query, dto.id)

    async def filter_by_group(self, group_id: int) -> list[Lesson] | None:
        query = "SELECT * FROM lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        if records is None:
            return None

        return [Lesson.from_mapping(record) for record in records]
