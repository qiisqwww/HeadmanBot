from dataclasses import dataclass

from src.modules.attendance.domain.enums.visit_status import VisitStatus

from .lesson import Lesson

__all__ = [
    "Attendance",
]


@dataclass(slots=True, frozen=True)
class Attendance:
    id: int
    student_id: int
    lesson: Lesson
    status: VisitStatus
