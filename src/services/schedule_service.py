from datetime import datetime, timedelta

from ..dto import Group
from ..mirea_api import MireaScheduleApi
from .base import Service
from .group_service import GroupService
from .lesson_service import LessonService

__all__ = [
    "ScheduleService",
]


class ScheduleService(Service):
    async def _recreate_schedule_for_group(self, group: Group, lesson_service: LessonService) -> None:
        first_day = datetime.today() - timedelta(days=datetime.today().weekday() % 7)
        api = MireaScheduleApi()

        for weekday in range(6):
            current_day = first_day + timedelta(days=weekday)
            lessons = await api.get_schedule(group.name, day=current_day)

            for lesson in lessons:
                await lesson_service.create(
                    discipline=lesson[0],
                    start_time=lesson[1],
                    group_id=group.id,
                    weekday=weekday,
                )

    async def recreate_shedule(self) -> None:
        """Recreate schedule for current week"""

        async with LessonService() as lesson_service:
            await lesson_service.delete_all_lessons()

        async with GroupService() as group_service:
            groups = await group_service.all()

        async with LessonService() as lesson_service:
            for group in groups:
                await self._recreate_schedule_for_group(group, lesson_service)
