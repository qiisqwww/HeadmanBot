from typing import final

from injector import inject

from src.modules.attendance.application.commands import CreateAttendanceCommand
from src.modules.attendance.application.contract import AttendanceModuleContract
from src.modules.common.domain import UniversityAlias

__all__ = [
    "AttendanceModuleContractImpl",
]


@final
class AttendanceModuleContractImpl(AttendanceModuleContract):
    _create_attendance_command: CreateAttendanceCommand

    @inject
    def __init__(self, create_attendance_command: CreateAttendanceCommand) -> None:
        self._create_attendance_command = create_attendance_command

    async def create_attendance(
        self, student_id: int, university_alias: UniversityAlias, group_id: int, group_name: str
    ) -> None:
        await self._create_attendance_command.execute(student_id, university_alias, group_id, group_name)
