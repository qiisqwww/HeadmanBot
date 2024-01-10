from src.repositories import LessonRepository
from src.services.interfaces import GroupService, LessonService, UniversityService

__all__ = [
    "LessonServiceImpl",
]


class LessonServiceImpl(LessonService):
    _lesson_repository: LessonRepository
    _group_service: GroupService
    _university_service: UniversityService

    def __init__(
        self, lesson_repository: LessonRepository, group_service: GroupService, university_service: UniversityService
    ) -> None:
        self._lesson_repository = lesson_repository
        self._group_service = group_service
        self._university_service = university_service

    async def recreate_lessons(self) -> None:
        """Recreate lessons for current day"""

        groups = await self._group_service.all()

        for group in groups:
            await self.try_fetch_schedule_for_group(group)
