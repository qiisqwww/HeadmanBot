from abc import ABC, abstractmethod

from src.modules.attendance.domain import StudentInfo

__all__ = [
    "StudentManagementGateway",
]


class StudentManagementGateway(ABC):
    @abstractmethod
    async def filter_student_info_by_group_id(self, group_id: int) -> dict[int, StudentInfo]:
        ...

    @abstractmethod
    async def update_is_checked_in_status(self, student_id: int, is_checked_in_previous: bool) -> None:
        ...
