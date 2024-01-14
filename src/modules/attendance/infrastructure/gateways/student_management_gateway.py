from typing import final

from injector import inject

from src.modules.attendance.application.gateways import StudentManagementGateway
from src.modules.attendance.domain import StudentInfo
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

    async def filter_student_info_by_group_id(self, group_id: int) -> dict[int, StudentInfo]:
        return {
            student_info["id"]: StudentInfo(**student_info)
            for student_info in (await self._contract.get_students_info(group_id))
        }
