from dataclasses import dataclass

from src.dto.models import GroupId, Student
from src.kernel import Model

from ..enums import VisitStatus
from ..models import LessonId

__all__ = [
    "GroupLessonVisitStatus",
]


@dataclass(frozen=True, slots=True)
class LessonAttendanceForGroup(Model):
    group_id: GroupId
    lesson_id: LessonId
    attendance: dict[Student, VisitStatus]
