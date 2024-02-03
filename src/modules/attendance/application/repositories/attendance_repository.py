from abc import ABC, abstractmethod

from src.modules.attendance.domain import Attendance, Lesson, VisitStatus

__all__ = [
    "AttendanceRepository",
]


class AttendanceRepository(ABC):
    @abstractmethod
    async def create_for_student(self, student_id: int, schedule: list[Lesson]) -> None:
        """Create all attendances for this student and its lessons."""

    @abstractmethod
    async def filter_by_student_id(self, student_id: int) -> list[Attendance]:
        ...

    @abstractmethod
    async def update_status(self, attendance_id: int, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def update_status_for_student(self, student_id: int, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def delete_all(self) -> None:
        ...
