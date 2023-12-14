from abc import abstractmethod

from src.dto import Group, GroupId, Lesson
from src.repositories import LessonRepository

from .group_service_interface import GroupService
from .service import Service
from .university_service_interface import UniversityService

__all__ = [
    "LessonService",
]


class LessonService(Service):
    @abstractmethod
    def __init__(
            self,
            lesson_repository: LessonRepository,
            group_service: GroupService,
            university_service: UniversityService
    ) -> None:
        ...

    @abstractmethod
    async def recreate_lessons(self) -> None:
        ...

    @abstractmethod
    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson] | None:
        ...

    @abstractmethod
    async def try_fetch_schedule_for_group(self, group: Group) -> None:
        ...
