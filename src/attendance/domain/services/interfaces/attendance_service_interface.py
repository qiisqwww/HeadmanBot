from abc import abstractmethod

from src.dto.models import GroupId, LessonId, Student, StudentId, StudentFullnameView
from src.dto.models.attendance_with_lesson import AttendanceWithLesson
from src.enums import VisitStatus
from src.repositories import AttendanceRepository

from .lesson_service_interface import LessonService
from .service import Service

__all__ = [
    "AttendanceService",
]


class AttendanceService(Service):
    @abstractmethod
    def __init__(self, attendance_repository: AttendanceRepository, lesson_service: LessonService) -> None:
        ...

    @abstractmethod
    async def recreate_attendances(self) -> None:
        ...

    @abstractmethod
    async def get_visit_status_for_group_students(
        self, group_id: GroupId, lesson_id: LessonId
    ) -> dict[StudentFullnameView, VisitStatus]:
        ...

    @abstractmethod
    async def get_visit_status_by_student_id_and_lesson(
        self, student_id: StudentId, lesson_id: LessonId
    ) -> VisitStatus:
        ...

    @abstractmethod
    async def update_visit_status_all(self, student_id: StudentId, new_status: VisitStatus) -> None:
        ...

    @abstractmethod
    async def filter_by_student_id(self, student_id: StudentId) -> list[AttendanceWithLesson]:
        ...

    @abstractmethod
    async def update_visit_status_for_lesson(
        self, student_id: StudentId, lesson_id: LessonId, new_status: VisitStatus
    ) -> None:
        ...

    @abstractmethod
    async def create_for_student(self, student: Student) -> None:
        ...
