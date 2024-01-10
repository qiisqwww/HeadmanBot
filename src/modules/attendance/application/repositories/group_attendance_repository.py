# from abc import ABC, abstractmethod
#
# from src.dto.models import GroupId
#
# from ..models import GroupLessonVisitStatus, LessonId
#
# __all__ = [
#     "GroupAttendanceRepository",
# ]
#
#
# class GroupAttendanceRepository(ABC):
#     @abstractmethod
#     async def find_group_visit_status_for_lesson(
#         self, group_id: GroupId, lesson_id: LessonId
#     ) -> GroupLessonVisitStatus:
#         ...
