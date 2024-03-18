from abc import ABC, abstractmethod

from src.modules.attendance.domain import Lesson
from src.modules.utils.schedule_api.domain import Schedule

__all__ = [
    "LessonRepository",
]


class LessonRepository(ABC):
    @abstractmethod
    async def filter_by_group_id(self, group_id: int) -> list[Lesson]:
        ...

    @abstractmethod
    async def create_for_group(self, group_id: int, schedule: list[Schedule]) -> list[Lesson]:
        ...

    @abstractmethod
    async def delete_all(self) -> None:
        ...

    @abstractmethod
    async def get_lessons_id_by_group_id(self, group_id: int) -> list[int] | None:
        ...

    @abstractmethod
    async def delete_lessons_by_group_id(self, group_id: int) -> None:
        ...
