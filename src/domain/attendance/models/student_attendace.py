from copy import deepcopy

from src.domain.student_management import Student

from ..enums import VisitStatus
from .attendance import Attendance
from .lesson import Lesson

__all__ = [
    "StudentAttendance",
]


class StudentAttendance:
    __slots__ = "_student", "_attendances"

    _student: Student
    _attendances: list[Attendance]

    def update_lesson_attendance(self, lesson: Lesson, new_status: VisitStatus) -> None:
        if not self._student.is_checked_in_today:
            self._student.is_checked_in_today = True

        for attendance in self._attendances:
            if attendance.lesson.id == lesson.id:
                attendance.status = new_status
                break

    def visit_all_lessons(self) -> None:
        if not self._student.is_checked_in_today:
            self._student.is_checked_in_today = True

        for attendance in self._attendances:
            attendance.status = VisitStatus.PRESENT

    def visit_none_lessons(self) -> None:
        if not self._student.is_checked_in_today:
            self._student.is_checked_in_today = True

        for attendance in self._attendances:
            attendance.status = VisitStatus.ABSENT

    @property
    def student(self) -> Student:
        return deepcopy(self._student)

    @property
    def attendances(self) -> list[Attendance]:
        return self._attendances.copy()
