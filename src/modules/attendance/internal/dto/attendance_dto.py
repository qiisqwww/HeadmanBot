from dataclasses import dataclass

from src.kernel.base import DTO
from src.modules.attendance.internal.enums import VisitStatus

__all__ = [
    "AttendanceDTO",
]


@dataclass(slots=True, frozen=True)
class AttendanceDTO(DTO):
    student_id: int
    lesson_id: int
    status: VisitStatus
