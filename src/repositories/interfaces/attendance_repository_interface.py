from abc import abstractmethod

from src.dto import Attendance, GroupId, LessonId, StudentId, StudentReadFullname
from src.enums import VisitStatus

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "AttendanceRepository",
]


class AttendanceRepository(PostgresRepository):
    @abstractmethod
    async def get_visit_status_by_student_id_and_lesson(
        self, student_id: StudentId, lesson_id: LessonId
    ) -> VisitStatus:
        ...

    @abstractmethod
    async def update_visit_status_all(self, student_id: StudentId, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def update_status_for_lesson(
        self, student_id: StudentId, lesson_id: LessonId, new_status: VisitStatus
    ) -> None:
        ...

    @abstractmethod
    async def delete_all_attendances(self) -> None:
        ...

    @abstractmethod
    async def create(self, student_id: StudentId, lesson_ids: list[LessonId]) -> None:
        ...

    @abstractmethod
    async def filter_by_student_id(self, student_id: StudentId) -> list[Attendance]:
        ...

    @abstractmethod
    async def get_visit_status_for_group_students(
        self, group_id: GroupId, lesson_id: LessonId
    ) -> dict[StudentReadFullname, VisitStatus]:
        ...
