from abc import abstractmethod
from datetime import time

from src.dto import GroupId, Lesson

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "LessonRepository",
]


class LessonRepository(PostgresRepository):
    @abstractmethod
    async def create(self, name: str, group_id: GroupId, start_time: time) -> None:
        ...

    @abstractmethod
    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson]:
        ...

    @abstractmethod
    async def delete_all_lessons(self) -> None:
        ...
