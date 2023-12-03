from dataclasses import dataclass
from typing import Any

from src.modules.attendance.internal.enums import VisitStatus

from .lesson_dto import LessonDTO

__all__ = [
    "Attendance",
]


@dataclass(slots=True, frozen=True)
class Attendance:
    student_id: int
    lesson: LessonDTO
    status: VisitStatus

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Attendance):
            return NotImplemented

        return self.lesson > other.lesson
