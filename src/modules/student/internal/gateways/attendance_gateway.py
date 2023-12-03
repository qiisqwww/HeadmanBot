from asyncpg.pool import PoolConnectionProxy

from src.kernel.base import PostgresService
from src.kernel.student_dto import StudentDTO
from src.modules.attendance.api.contract import AttendanceContract
from src.modules.group.api.dto import GroupDTO

__all__ = [
    "AttendanceGateway",
]


class AttendanceGateway(PostgresService):
    _attendance_contract: AttendanceContract

    def __init__(self, con: PoolConnectionProxy) -> None:
        super().__init__(con)
        self._attendance_contract = AttendanceContract(con)

    async def create_attendances_for_student(self, student: StudentDTO, group: GroupDTO) -> None:
        await self._attendance_contract.create_attendances_for_student(student, group)
