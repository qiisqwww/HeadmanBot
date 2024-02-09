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
    async def note_student_attendance(self, student_id: int) -> None:
        ...
