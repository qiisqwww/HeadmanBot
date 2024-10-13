from injector import inject

from src.common import UseCase
from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.attendance.domain import Attendance

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
