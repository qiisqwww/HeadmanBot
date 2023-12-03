from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.attendance.internal.services import AttendanceService, LessonService
from src.modules.group.api.dto import GroupDTO

__all__ = [
    "AttendanceContract",
]


class AttendanceContract(PostgresService):
    _lesson_service: LessonService
    _attendance_service: AttendanceService

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._lesson_service = LessonService(self._con)
        self._attendance_service = AttendanceService(self._con)

    async def create_attendances_for_student(self, student: StudentDTO, group: GroupDTO) -> None:
        await self._lesson_service.try_fetch_schedule_for_group(group)
        await self._attendance_service.create(student)
