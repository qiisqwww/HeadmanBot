from abc import ABC, abstractmethod

from src.dto.models import GroupId, StudentFullnameView, StudentId

from ..enums import VisitStatus
from ..models import Attendance, AttendanceId, LessonId

__all__ = [
    "AttendanceRepository",
]


class AttendanceRepository(ABC):
    @abstractmethod
    async def create_for_student(self, student_id: StudentId) -> None:
        """Create all attendances for this student and its lessons."""

    @abstractmethod
    async def filter_by_student_id(self, student_id: StudentId) -> list[Attendance]:
        ...

    @abstractmethod
    async def find_or_fail(self, attendance_id: AttendanceId) -> Attendance:
        ...

    @abstractmethod
    async def update_status(self, attendance_id: AttendanceId, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def update_status_for_student(self, student_id: StudentId, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def delete_all(self) -> None:
        ...

    @abstractmethod
    async def get_visit_status_for_group_students(
        self, group_id: GroupId, lesson_id: LessonId
    ) -> dict[StudentFullnameView, VisitStatus]:
        ...
