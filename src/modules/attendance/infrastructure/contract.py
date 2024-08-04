from typing import final

from injector import inject

from src.modules.attendance.application.commands import CreateAttendanceCommand
from src.modules.attendance.application.repositories import AttendanceRepository, LessonRepository
from src.modules.attendance.contract import AttendanceModuleContract
from src.modules.common.domain import UniversityAlias

__all__ = [
    "AttendanceModuleContractImpl",
]


@final
class AttendanceModuleContractImpl(AttendanceModuleContract):
    _create_attendance_command: CreateAttendanceCommand
    _attendance_repository: AttendanceRepository
    _lesson_repository: LessonRepository

    @inject
    def __init__(
            self,
            create_attendance_command: CreateAttendanceCommand,
            attendance_repository: AttendanceRepository,
            lesson_repository: LessonRepository,
    ) -> None:
        self._create_attendance_command = create_attendance_command
        self._attendance_repository = attendance_repository
        self._lesson_repository = lesson_repository

    async def create_attendance(
        self,
        student_id: int,
        university_alias: UniversityAlias,
        group_id: int,
        group_name: str,
    ) -> None:
        await self._create_attendance_command.execute(student_id, university_alias, group_id, group_name)

    async def delete_attendance_by_student_id(self, student_id: int) -> None:
        await self._attendance_repository.delete_attendance_by_student_id(student_id)

    async def delete_attendance_by_group_id(self, group_id: int) -> None:
        await self._attendance_repository.delete_attendance_by_group_id(group_id)

    async def delete_lessons_by_group_id(self, group_id: int) -> None:
        return await self._lesson_repository.delete_lessons_by_group_id(group_id)
