from dataclasses import dataclass
from typing import Any

from src.enums import VisitStatus

from .lesson import Lesson
from .student import StudentId

__all__ = [
    "AttendanceWithLesson",
]


@dataclass(slots=True, frozen=True)
class AttendanceWithLesson:
    student_id: StudentId
    lesson: Lesson
    status: VisitStatus

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, AttendanceWithLesson):
            return NotImplemented

        return self.lesson > other.lesson
