from datetime import datetime, time, timezone

from src.api import ScheduleApi
from src.config import DEBUG
from src.dto import Group, Lesson, Student
from src.enums.university_id import UniversityId
from src.enums.weekday import Weekday

from .group_service import GroupService
from .service import Service

__all__ = [
    "LessonService",
]


def create_time_with_timezone(time_without_tz: time) -> time:
    return time(hour=time_without_tz.hour, minute=time_without_tz.minute, tzinfo=timezone.utc)


class LessonService(Service):
    async def recreate_lessons(self) -> None:
        """Recreate lessons for current week"""

        await self._delete_all_lessons()

        groups = await GroupService(self._con).all()

        for group in groups:
            await self._recreate_schedule_for_group(group)

    async def filter_by_student(self, student: Student) -> list[Lesson]:
        return await self._filter_by_group_id(student.group_id)

    async def filter_by_group(self, group: Group) -> list[Lesson]:
        return await self._filter_by_group_id(group.id)

    async def _filter_by_group_id(self, group_id: int) -> list[Lesson]:
        query = "SELECT * FROM lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        lessons = [Lesson.from_mapping(record) for record in records]
        lessons.sort()

        return lessons

    async def _create(self, name: str, group_id: int, start_time: time) -> None:
        query = "INSERT INTO lessons (name, group_id, start_time) VALUES($1, $2, $3)"
        await self._con.execute(query, name, group_id, start_time)

    async def _recreate_schedule_for_group(self, group: Group) -> None:
        today = datetime.today().weekday()
        if DEBUG:
            today = datetime(year=2023, month=10, day=11).weekday()

        api = ScheduleApi(UniversityId.MIREA)

        lessons = await api.fetch_schedule(group.name, weekday=Weekday(today))
        for lesson in lessons:
            await self._create(
                name=lesson.lesson_name,
                start_time=create_time_with_timezone(lesson.start_time),
                group_id=group.id,
            )

    async def _delete_all_lessons(self) -> None:
        query = "TRUNCATE TABLE lessons CASCADE"
        await self._con.execute(query)
