from abc import abstractmethod

from src.modules.attendance.domain import StudentInfo
from src.modules.common.application import Dependency

__all__ = [
    "StudentManagementGateway",
]


class StudentManagementGateway(Dependency):
    @abstractmethod
    async def filter_student_info_by_group_id(self, group_id: int) -> dict[int, StudentInfo]:
        ...
