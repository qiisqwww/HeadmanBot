from dataclasses import dataclass

from src.enums import VisitStatus

from .dto import DTO
from .lesson import LessonId
from .student import StudentId

__all__ = [
    "Attendance",
]


@dataclass(slots=True, frozen=True)
class Attendance(DTO):
    student_id: StudentId
    lesson_id: LessonId
    status: VisitStatus
