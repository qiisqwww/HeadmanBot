from datetime import datetime, time, timezone

from asyncpg.pool import PoolConnectionProxy

from src.config import DEBUG
from src.external.apis import ScheduleApi, Weekday
from src.kernel.base import PostgresService
from src.modules.attendance.internal.dto import LessonDTO
from src.modules.attendance.internal.gateways import UniversityGateway
from src.modules.group.api.dto import GroupDTO

__all__ = [
    "LessonService",
]


def create_time_with_timezone(time_without_tz: time) -> time:
    return time(hour=time_without_tz.hour, minute=time_without_tz.minute, tzinfo=timezone.utc)


class LessonService(PostgresService):
    _university_gateway: UniversityGateway

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_gateway = UniversityGateway(con)

    async def recreate_lessons(self) -> None:
        """Recreate lessons for current day"""

        await self._delete_all_lessons()

        groups = await GroupService(self._con).all()

        for group in groups:
            await self.fetch_schedule_for_group(group)

    async def filter_by_student(self, student: Student) -> list[LessonDTO]:
        query = "SELECT * FROM lesson as le JOIN students_groups as sg ON le.group_id = sg.group_id WHERE sg.student_id = $1"
        records = await self._con.fetch(query, student.telegram_id)
        return [LessonDTO.from_mapping(record) for record in records]

    async def filter_by_group(self, group: GroupDTO) -> list[LessonDTO]:
        return await self._filter_by_group_id(group.id)

    async def _filter_by_group_id(self, group_id: int) -> list[LessonDTO]:
        query = "SELECT * FROM lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        lessons = [LessonDTO.from_mapping(record) for record in records]
        lessons.sort()

        return lessons

    async def _create(self, name: str, group_id: int, start_time: time) -> None:
        query = "INSERT INTO lessons (name, group_id, start_time) VALUES($1, $2, $3)"
        await self._con.execute(query, name, group_id, start_time)

    async def fetch_schedule_for_group(self, group: GroupDTO) -> None:
        today = datetime.today().weekday()
        if DEBUG:
            today = datetime(year=2023, month=10, day=11).weekday()

        university = await self._university_gateway.get_university_by_group(group)
        api = ScheduleApi(university.alias)

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
