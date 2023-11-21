from dataclasses import dataclass
from typing import Any, Mapping, Self

from ..enums import VisitStatus
from .lesson import Lesson

__all__ = [
    "Attendance",
]


@dataclass(slots=True)
class Attendance:
    student_id: int
    lesson: Lesson
    status: VisitStatus

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Attendance):
            return NotImplemented

        return self.lesson > other.lesson

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            lesson=Lesson.from_mapping(data),
            status=VisitStatus(data["visit_status"]),
            student_id=data["student_id"],
        )
