from dataclasses import dataclass
from typing import Any, Mapping, NewType

from src.dto.models import StudentId
from src.kernel import Model

from ..enums import VisitStatus
from .lesson import Lesson

__all__ = [
    "Attendance",
    "AttendanceId",
]

AttendanceId = NewType("AttendanceId", int)


@dataclass(frozen=True, slots=True)
class Attendance(Model):
    id: AttendanceId
    student_id: StudentId
    lesson: Lesson
    status: VisitStatus

    @classmethod
    def from_mapping(cls, data: Mapping) -> "Attendance":
        lesson = Lesson(
            id=data["lesson_id"],
            group_id=data["group_id"],
            name=data["name"],
            start_time=data["start_time"],
        )

        return cls(
            id=data["id"],
            student_id=data["student_id"],
            lesson=lesson,
            status=VisitStatus(data["status"]),
        )

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Attendance):
            return NotImplemented

        return self.lesson > other.lesson
