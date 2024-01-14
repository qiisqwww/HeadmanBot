from abc import abstractmethod

from src.modules.attendance.domain import LessonAttendanceForGroup, StudentInfo
from src.modules.common.application import Dependency

__all__ = [
    "GroupAttendanceRepository",
]


class GroupAttendanceRepository(Dependency):
    @abstractmethod
    async def find_group_visit_status_for_lesson(
        self, group_id: int, lesson_id: int, students_info: dict[int, StudentInfo]
    ) -> LessonAttendanceForGroup:
        ...
