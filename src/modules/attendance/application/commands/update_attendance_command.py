from injector import inject

from src.modules.attendance.application.gateways import StudentManagementGateway
from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.attendance.domain import VisitStatus
from src.modules.common.application import Dependency, UnitOfWork

__all__ = [
    "UpdateAttendanceCommand",
]


class UpdateAttendanceCommand(Dependency):
    _repostiory: AttendanceRepository
    _gateway: StudentManagementGateway
    _uow: UnitOfWork

    @inject
    def __init__(self, repository: AttendanceRepository, gateway: StudentManagementGateway, uow: UnitOfWork) -> None:
        self._repostiory = repository
        self._gateway = gateway
        self._uow = uow

    async def execute(self, student_id: int, is_checked_in: bool, attendance_id: int, new_status: VisitStatus) -> None:
        async with self._uow:
            await self._gateway.update_is_checked_in_status(student_id, is_checked_in)
            await self._repostiory.update_status(attendance_id, new_status)
