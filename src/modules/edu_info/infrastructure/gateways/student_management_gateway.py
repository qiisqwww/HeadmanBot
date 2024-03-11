from typing import final

from injector import inject

from src.modules.edu_info.application.gateways import StudentManagementGateway
from src.modules.student_management.contract import StudentManagementContract

__all__ = [
    "StudentManagementGateway",
]


@final
class StudentManagementGatewayImpl(StudentManagementGateway):
    _contract: StudentManagementContract

    @inject
    def __init__(self, contract: StudentManagementContract) -> None:
        self._contract = contract

    async def get_headman_by_group_id(self, group_id: int) -> dict:
        return await self._contract.get_headman_by_group_id(group_id)
