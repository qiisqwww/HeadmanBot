from src.dto.attendance import Attendance
from src.dto.lesson import Lesson

from ..enums import VisitStatus
from .base import Service
from .group_service import GroupService
from .lesson_service import LessonService
from .student_service import StudentService

__all__ = [
    "AttendanceService",
]


class AttendanceService(Service):
    async def create(self, student_id: int) -> None:
        async with StudentService() as student_service:
            student = await student_service.get(student_id)

        async with GroupService() as group_service:
            group = await group_service.get(student.group_id)

        async with LessonService() as lesson_service:
            lessons = await lesson_service.get_by_group(group.id)

        query = "INSERT INTO attendance VALUES($1, $2, $3)"

        for lesson in lessons:
            await self._con.execute(query, student_id, lesson.id, VisitStatus.NOT_CHECKED)

    async def set_status(self, student_id: int, lesson_id: int, visit_status: VisitStatus) -> None:
        query = "UPDATE attendance SET visit_status = $1 WHERE student_id = $2 AND WHERE lesson_id = $3"

        await self._con.execute(query, visit_status, student_id, lesson_id)

    async def _delete_all_attendance(self) -> None:
        query = "TRUNCATE TABLE attendance"
        await self._con.execute(query)

    async def recreate_all_attendance(self) -> None:
        """Recreate attendance for current day"""

        await self._delete_all_attendance()

        async with StudentService() as student_service:
            students = await student_service.all()

        for student in students:
            await self.create(student.telegram_id)

    async def set_status_for_all_lessons(self, student_id: int, visit_status: VisitStatus) -> None:
        async with StudentService() as student_service:
            lessons = await student_service.get_schedule(student_id)

        for lesson in lessons:
            await self.set_status(student_id, lesson.id, visit_status)

    async def get(self, student_id: int) -> Attendance:
        query = "SELECT lesson_id,visit_status FROM attendance WHERE student_id = $1"
        records = await self._con.fetch(query, student_id)

        lessons_with_status: list[tuple[Lesson, VisitStatus]] = []

        for record in records:
            async with LessonService() as lesson_service:
                lesson = await lesson_service.get(record["lessond_id"])
                lessons_with_status.append((lesson, VisitStatus(record["visit_status"])))

        return Attendance(
            student_id=student_id,
            lessons=lessons_with_status,
        )
