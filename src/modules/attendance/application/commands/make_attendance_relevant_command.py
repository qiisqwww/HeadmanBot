from typing import final

from injector import inject

from src.modules.attendance.application.gateways import EduInfoModuleGateway
from src.modules.attendance.application.gateways.student_management_gateway import (
    StudentManagementGateway,
)
from src.modules.attendance.application.repositories import (
    AttendanceRepository,
    LessonRepository,
)
from src.modules.common.application import NoArgsUseCase, UnitOfWork
from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.infrastructure.exceptions import ScheduleApiError

__all__ = [
    "MakeAttendanceRelevantCommand",
]


@final
class MakeAttendanceRelevantCommand(NoArgsUseCase):
    _attendance_repository: AttendanceRepository
    _lesson_repository: LessonRepository
    _edu_info_gateway: EduInfoModuleGateway
    _student_management_gateway: StudentManagementGateway
    _schedule_api: type[ScheduleAPI]
    _notifier: BotNotifier
    _uow: UnitOfWork

    @inject
    def __init__(
        self,
        attendance_repository: AttendanceRepository,
        lesson_repository: LessonRepository,
        edu_info_gateway: EduInfoModuleGateway,
        student_management_gateway: StudentManagementGateway,
        uow: UnitOfWork,
        schedule_api: type[ScheduleAPI],
        notifier: BotNotifier,
    ) -> None:
        self._schedule_api = schedule_api
        self._attendance_repository = attendance_repository
        self._lesson_repository = lesson_repository
        self._edu_info_gateway = edu_info_gateway
        self._student_management_gateway = student_management_gateway
        self._uow = uow
        self._notifier = notifier

    async def execute(self) -> None:
        async with self._uow:
            await self._lesson_repository.delete_all()
            await self._attendance_repository.delete_all()

            groups = await self._edu_info_gateway.fetch_all_groups()

            for group in groups:
                schedule_api = self._schedule_api(group.university_alias)

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

                    students = await self._student_management_gateway.filter_student_info_by_group_id(
                        group.id,
                    )

                    for student_id in students:
                        await self._attendance_repository.create_for_student(
                            student_id,
                            group_schedule,
                        )
