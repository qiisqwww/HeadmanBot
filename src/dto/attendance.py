from dataclasses import dataclass

from ..enums import VisitStatus
from .lesson import Lesson

__all__ = [
    "Attendance",
]


@dataclass(slots=True)
class Attendance:
    student_id: int
    lessons: list[tuple[Lesson, VisitStatus]]
