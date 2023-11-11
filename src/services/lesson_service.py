from datetime import datetime, time, timedelta

from src.repositories.group_repository import GroupRepository

from ..dto import Group
from ..mirea_api import MireaScheduleApi
from ..repositories import LessonRepository
from .base import Service

__all__ = [
    "LessonService",
]


class LessonService(Service):
    async def create(self, discipline: str, group_id: int, start_time: time, weekday: int) -> None:
        lesson_repository = LessonRepository(self._con)
        if await lesson_repository.find(discipline, group_id, start_time, weekday) is None:
            return None

        query = "INSERT INTO lessons (discipline, group_id, start_time, weekday) VALUES($1, $2, $3, $4)"
        await self._con.execute(query, discipline, group_id, start_time, weekday)

    async def delete_all_lessons(self) -> None:
        query = "TRUNCATE TABLE lessons CASCADE"
        await self._con.execute(query)

    async def _recreate_schedule_for_group(self, group: Group) -> None:
        lesson_service = LessonService(self._con)
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

    async def recreate_lessons(self) -> None:
        """Recreate lessons for current week"""

        lesson_service = LessonService(self._con)
        await lesson_service.delete_all_lessons()

        groups = await GroupRepository(self._con).all()

        for group in groups:
            await self._recreate_schedule_for_group(group)
