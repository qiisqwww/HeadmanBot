from dataclasses import dataclass
from typing import Any

from ..enums import VisitStatus
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

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Attendance):
            return NotImplemented

        return self.lesson > other.lesson
