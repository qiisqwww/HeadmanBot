from injector import inject

from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.attendance.domain import Attendance
from src.modules.common.application import UseCase

__all__ = [
    "GetStudentAttendanceQuery",
]


class GetStudentAttendanceQuery(UseCase):
    _repository: AttendanceRepository

    @inject
    def __init__(self, repository: AttendanceRepository) -> None:
        self._repository = repository

    async def execute(self, student_id: int) -> list[Attendance]:
        return await self._repository.filter_by_student_id(student_id)
