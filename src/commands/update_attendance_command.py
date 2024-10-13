from injector import inject

from src.common import UnitOfWork, UseCase
from src.modules.attendance.application.gateways import StudentManagementGateway
from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.attendance.domain import VisitStatus

__all__ = [
    "UpdateAttendanceCommand",
]


class UpdateAttendanceCommand(UseCase):
    _repostiory: AttendanceRepository
    _gateway: StudentManagementGateway
    _uow: UnitOfWork

    @inject
    def __init__(self, repository: AttendanceRepository, gateway: StudentManagementGateway, uow: UnitOfWork) -> None:
        self._repostiory = repository
        self._gateway = gateway
        self._uow = uow

    async def execute(self, student_id: int, attendance_id: int, new_status: VisitStatus) -> None:
        async with self._uow:
            await self._gateway.note_student_attendance(student_id)
            await self._repostiory.update_status(attendance_id, new_status)
