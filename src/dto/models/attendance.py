from dataclasses import dataclass

from src.enums import VisitStatus

from .lesson import LessonId
from .model import Model
from .student import StudentId

__all__ = [
    "Attendance",
]


@dataclass(slots=True, frozen=True)
class Attendance(Model):
    student_id: StudentId
    lesson_id: LessonId
    status: VisitStatus
