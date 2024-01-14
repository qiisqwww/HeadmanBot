from abc import ABC, abstractmethod

from src.modules.attendance.domain import Lesson
from src.modules.common.application.schedule_api import Schedule

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

    # @abstractmethod
    # async def delete_all(self) -> None:
    #     ...
