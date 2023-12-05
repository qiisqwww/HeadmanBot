from datetime import datetime, time, timezone
from logging import DEBUG

from src.dto import Group, GroupId, Lesson
from src.external.apis import ScheduleApi, Weekday
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

    async def filter_by_group_id(self, group_id: GroupId) -> list[Lesson]:
        return await self._lesson_repository.filter_by_group_id(group_id)

    async def try_fetch_schedule_for_group(self, group: Group) -> None:
        if await self._group_has_schedule(group.id):
            return
        today = datetime.today().weekday()

        if DEBUG:
            today = datetime(year=2023, month=10, day=11).weekday()

        university = await self._university_service.get_by_id(group.university_id)

        api = ScheduleApi(university.alias)
        lessons = await api.fetch_schedule(group.name, weekday=Weekday(today))

        for lesson in lessons:
            await self._lesson_repository.create(
                name=lesson.lesson_name,
                start_time=self._create_time_with_timezone(lesson.start_time),
                group_id=group.id,
            )

    @staticmethod
    def _create_time_with_timezone(time_without_tz: time) -> time:
        return time(hour=time_without_tz.hour, minute=time_without_tz.minute, tzinfo=timezone.utc)

    async def _group_has_schedule(self, group_id: GroupId) -> bool:
        lessons = await self._lesson_repository.filter_by_group_id(group_id)
        return bool(lessons)
