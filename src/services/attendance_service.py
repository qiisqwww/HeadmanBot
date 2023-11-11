from src.dto import Attendance, StudentAttendaces
from src.enums import VisitStatus

from .base import Service
from .student_service import StudentService

__all__ = [
    "AttendanceService",
]


class AttendanceService(Service):
    async def create(self, student_id: int) -> None:
        lessons = await StudentService(self._con).get_schedule(student_id)

        query = "INSERT INTO attendance VALUES($1, $2, $3)"

        await self._con.executemany(query, ((student_id, lesson.id, VisitStatus.NOT_CHECKED) for lesson in lessons))

    async def recreate_all_attendances(self) -> None:
        """Recreate attendances for current day"""

        await self._delete_all_attendances()

        student_service = StudentService(self._con)
        students = await student_service.all()

        for student in students:
            await self.create(student.telegram_id)

    async def update_visit_status(
        self, student_attendaces: StudentAttendaces, attendance: Attendance, new_status: VisitStatus
    ) -> None:
        for st_attendance in student_attendaces:
            if st_attendance.status == VisitStatus.NOT_CHECKED:
                await self._set_status(st_attendance, VisitStatus.NOT_VISIT)

        await self._set_status(attendance, new_status)

    async def update_visit_status_for_all_lessons(
        self, student_attendaces: StudentAttendaces, new_status: VisitStatus
    ) -> None:
        for st_attendance in student_attendaces:
            await self._set_status(st_attendance, new_status)

    async def _set_status(self, attendance: Attendance, new_status: VisitStatus) -> None:
        query = "UPDATE attendance SET visit_status = $1 WHERE lesson_id = $2 AND student_id = $3"
        await self._con.execute(query, new_status, attendance.lesson.id, attendance.student_id)

    async def _delete_all_attendances(self) -> None:
        query = "TRUNCATE TABLE attendance"
        await self._con.execute(query)
