from typing import final
from src.modules.attendance.application.gateways.student_management_gateway import StudentManagementGateway

from src.modules.common.application import UseCase, UnitOfWork
from src.modules.common.application.schedule_api import ScheduleAPI

from src.modules.attendance.application.repositories import LessonRepository, AttendanceRepository
from src.modules.attendance.application.gateways import EduInfoModuleGateway

__all__ = [
    "MakeAttendanceRelevantCommand",
]

@final
class MakeAttendanceRelevantCommand(UseCase):
    _attendance_repository: AttendanceRepository
    _lesson_repository: LessonRepository
    _edu_info_gateway: EduInfoModuleGateway
    _student_management_gateway: StudentManagementGateway
    _schedule_api: type[ScheduleAPI]
    _uow: UnitOfWork

    def __init__(self, 
                 attendance_repostory: AttendanceRepository,
                 lesson_repository: LessonRepository,
                 edu_info_gateway: EduInfoModuleGateway,
                 uow: UnitOfWork,
                 schedule_api: type[ScheduleAPI]
                    ) -> None:
        self._schedule_api = schedule_api
        self._attendance_repository = attendance_repostory 
        self._lesson_repository = lesson_repository
        self._edu_info_gateway = edu_info_gateway
        self._uow = uow

    async def execute(self) -> None:
        async with self._uow:
            await self._lesson_repository.delete_all()
            await self._attendance_repository.delete_all()

            groups = await self._edu_info_gateway.fetch_all_groups()

            for group in groups:
                schedule_api = self._schedule_api(group.alias)

                fetched_schedule = await schedule_api.fetch_schedule(group.name)
                group_schedule = await self._lesson_repository.create_for_group(group.id, fetched_schedule)

                students = await self._student_management_gateway.filter_student_info_by_group_id(group.id)

                for student_id in students:
                    await self._attendance_repository.create_for_student(student_id, group_schedule)
