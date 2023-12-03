from datetime import datetime, time, timezone

from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.config import DEBUG
from src.kernel.external.apis import ScheduleApi, Weekday
from src.kernel.student_dto import StudentDTO
from src.modules.attendance.internal.dto import LessonDTO
from src.modules.attendance.internal.gateways import GroupGateway, UniversityGateway
from src.modules.group.api.dto import GroupDTO

__all__ = [
    "LessonService",
]


def create_time_with_timezone(time_without_tz: time) -> time:
    return time(hour=time_without_tz.hour, minute=time_without_tz.minute, tzinfo=timezone.utc)


class LessonService(PostgresService):
    _university_gateway: UniversityGateway
    _group_gateway: GroupGateway

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._university_gateway = UniversityGateway(con)
        self._group_gateway = GroupGateway(con)

    async def recreate_lessons(self) -> None:
        """Recreate lessons for current day"""

        await self._delete_all_lessons()

        groups = await self._group_gateway.get_all_groups()

        for group in groups:
            await self.try_fetch_schedule_for_group(group)

    async def filter_by_student(self, student: StudentDTO) -> list[LessonDTO]:
        query = "SELECT * FROM attendances.lessons WHERE group_id = $1"
        records = await self._con.fetch(query, student.group_id)

        return [LessonDTO.from_mapping(record) for record in records]

    async def filter_by_group_id(self, group_id: int) -> list[LessonDTO]:
        query = "SELECT * FROM attendances.lessons WHERE group_id = $1"
        records = await self._con.fetch(query, group_id)

        lessons = [LessonDTO.from_mapping(record) for record in records]
        lessons.sort()

        return lessons

    async def try_fetch_schedule_for_group(self, group: GroupDTO) -> None:
        if await self._group_has_schedule(group):
            return
        today = datetime.today().weekday()
        if DEBUG:
            today = datetime(year=2023, month=10, day=11).weekday()

        university = await self._university_gateway.get_university_by_id(group.university_id)

        api = ScheduleApi(university.alias)
        lessons = await api.fetch_schedule(group.name, weekday=Weekday(today))

        for lesson in lessons:
            await self._create(
                name=lesson.lesson_name,
                start_time=create_time_with_timezone(lesson.start_time),
                group_id=group.id,
            )

    async def _create(self, name: str, group_id: int, start_time: time) -> None:
        query = "INSERT INTO attendances.lessons (name, group_id, start_time) VALUES($1, $2, $3)"
        await self._con.execute(query, name, group_id, start_time)

    async def _delete_all_lessons(self) -> None:
        query = "TRUNCATE TABLE attendances.lessons CASCADE"
        await self._con.execute(query)

    async def _group_has_schedule(self, group: GroupDTO) -> bool:
        query = "SELECT id FROM attendances.lessons WHERE group_id = $1 LIMIT 1"

        lesson_id = await self._con.fetchval(query, group.id)

        return lesson_id is not None
