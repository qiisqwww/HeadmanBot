from dataclasses import dataclass
from datetime import date
from typing import NewType, Mapping, Self, Any

from src.dto.enums.visit_status import VisitStatus
from .group import GroupId
from .lesson import Lesson, LessonId
from .student import StudentId

__all__ = [
    "Attendance",
    "AttendanceId",
]

AttendanceId = NewType("AttendanceId", int)


@dataclass(slots=True, frozen=True)
class Attendance:
    id: AttendanceId
    student_id: StudentId
    lesson: Lesson
    date: date
    status: VisitStatus

    @classmethod
    def from_record(cls, record: Mapping[str, Any], student_id: StudentId | None = None) -> Self:
        return Attendance(
            id=AttendanceId(record["id"]),
            student_id=student_id if student_id else StudentId(record["student_id"]),
            status=VisitStatus(record["status"]),
            date=record["date"],
            lesson=Lesson(
                id=LessonId(record["lesson_id"]),
                group_id=GroupId(record["group_id"]),
                start_time=record["start_time"],
                name=record["name"],
            ),
        )
