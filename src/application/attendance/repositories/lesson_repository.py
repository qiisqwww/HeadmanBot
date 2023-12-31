from abc import ABC, abstractmethod

from src.dto.models import GroupId

from ..models import Lesson
from .dto import CreateLessonDTO

__all__ = [
    "LessonRepository",
]


class LessonRepository(ABC):
    @abstractmethod
    async def create(self, data: CreateLessonDTO) -> Lesson:
        ...

    @abstractmethod
    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson]:
        ...

    @abstractmethod
    async def delete_all(self) -> None:
        ...
