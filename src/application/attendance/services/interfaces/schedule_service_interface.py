from abc import ABC, abstractmethod

from src.dto.models import Group

from ...models import Schedule
from ...repositories import LessonRepository

__all__ = [
    "ScheduleService",
]


class ScheduleService(ABC):
    @abstractmethod
    def __init__(self, lesson_repository: LessonRepository) -> None:
        ...

    @abstractmethod
    async def fetch_schedule_for_group(self, group: Group) -> None:
        ...

    @abstractmethod
    async def get_group_schedule(self, group: Group) -> Schedule:
        ...

    @abstractmethod
    async def update_schedule(self) -> None:
        ...
