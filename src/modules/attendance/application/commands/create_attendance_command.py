from datetime import datetime

from injector import inject
from loguru import logger

from src.modules.attendance.application.repositories import (
    AttendanceRepository,
    LessonRepository,
)
from src.modules.common.application import Dependency
from src.modules.common.application.schedule_api import ScheduleAPI, Weekday
from src.modules.common.domain import UniversityAlias
from src.modules.common.infrastructure import DEBUG

__all__ = [
    "CreateAttendanceCommand",
]


class CreateAttendanceCommand(Dependency):
    _attendance_repository: AttendanceRepository
    _lesson_repository: LessonRepository
    _schedule_api: type[ScheduleAPI]

    @inject
    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        lesson_repository: LessonRepository,
        schedule_api: type[ScheduleAPI],
    ) -> None:
        self._attendance_repository = attendance_repository
        self._lesson_repository = lesson_repository
        self._schedule_api = schedule_api

    async def execute(self, student_id: int, university_alias: UniversityAlias, group_id: int, group_name: str) -> None:
        group_schedule = await self._lesson_repository.filter_by_group_id(group_id)

        if not group_schedule:
            today = datetime.today().weekday()

            if DEBUG:
                today = datetime(year=2023, month=10, day=11).weekday()

            schedule_api = self._schedule_api(university_alias)
            logger.error("Before")
            fetched_schedule = await schedule_api.fetch_schedule(group_name, Weekday(today))
            logger.error(fetched_schedule)
            logger.error("After")

            group_schedule = await self._lesson_repository.create_for_group(group_id, fetched_schedule)

        await self._attendance_repository.create_for_student(student_id, group_schedule)
