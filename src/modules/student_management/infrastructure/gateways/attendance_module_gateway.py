from typing import final

from injector import inject

from src.modules.attendance.application.contract import AttendanceModuleContract
from src.modules.common.domain import UniversityAlias
from src.modules.student_management.application.gateways import AttendanceModuleGateway

__all__ = [
    "AttendanceModuleGatewayImpl",
]


@final
class AttendanceModuleGatewayImpl(AttendanceModuleGateway):
    _contract: AttendanceModuleContract

    @inject
    def __init__(self, contract: AttendanceModuleContract) -> None:
        self._contract = contract

    async def create_attendance(
        self, student_id: int, university_alias: UniversityAlias, group_id: int, group_name: str
    ) -> None:
        await self._contract.create_attendance(student_id, university_alias, group_id, group_name)
