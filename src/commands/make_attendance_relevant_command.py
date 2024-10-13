from datetime import datetime
from typing import final

from src.common.bot_notifier import BotNotifier
from src.common.database import DbContext
from src.common.uow import UnitOfWork
from src.common.use_case import NoArgsUseCase
from src.repositories import (
    AttendanceRepository,
    LessonRepository,
    GroupRepository,
    StudentRepository,
)
from src.utils.schedule_api.application import ScheduleAPI
from src.utils.schedule_api.infrastructure import ScheduleApiError

__all__ = [
    "MakeAttendanceRelevantCommand",
]


@final
class MakeAttendanceRelevantCommand(NoArgsUseCase):
    _attendance_repository: AttendanceRepository
    _group_repository: GroupRepository
    _student_repository: StudentRepository
    _notifier: BotNotifier
    _uow: UnitOfWork

    def __init__(self, con: DbContext) -> None:
        self._attendance_repository = AttendanceRepository(con)
        self._group_repository = GroupRepository(con)
        self._lesson_repository = LessonRepository(con)
        self._student_repository = StudentRepository(con)
        self._uow = UnitOfWork(con)
        self._notifier = BotNotifier()

    async def execute(self) -> None:
        async with self._uow:
            day = datetime.now().date()
            groups = await self._group_repository.all()

            for group in groups:
                schedule_api = ScheduleAPI(group.university.alias)

                try:
                    fetched_schedule = await schedule_api.fetch_schedule(group.name)
                except ScheduleApiError as e:
                    await self._notifier.notify_about_job_exception(e, "MakeAttendanceRelevantJob")
                    continue

                if fetched_schedule:
                    group_schedule = await self._lesson_repository.create_for_group(
                        group.id,
                        fetched_schedule,
                    )

                    students = await self._student_repository.filter_by_group_id(group.id)
                    for student_id in students:
                        await self._attendance_repository.create_for_student(
                            student_id,
                            group_schedule,
                            day,
                        )
