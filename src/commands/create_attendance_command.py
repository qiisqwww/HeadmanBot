from injector import inject
from src.modules.utils.schedule_api.application import ScheduleAPI

from src.common import UniversityAlias
from src.common import UseCase
from src.modules.attendance.application.repositories import (
    AttendanceRepository,
    LessonRepository,
)

__all__ = [
    "CreateAttendanceCommand",
]


class CreateAttendanceCommand(UseCase):
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
            schedule_api = self._schedule_api(university_alias)
            fetched_schedule = await schedule_api.fetch_schedule(group_name)

            group_schedule = await self._lesson_repository.create_for_group(group_id, fetched_schedule)

        await self._attendance_repository.create_for_student(student_id, group_schedule)
