from typing import Mapping

from src.common.services import Service
from src.dto import Attendance, Lesson, Student
from src.enums import VisitStatus

from .lesson_service import LessonService
from .student_service import StudentService

__all__ = [
    "AttendanceService",
]


class AttendanceService(Service):
    async def recreate_attendances(self) -> None:
        """Recreate attendances for current day"""

        await self._delete_all_attendances()

        student_service = StudentService(self._con)
        students = await student_service.all()

        for student in students:
            await self._create(student)

    async def filter_by_student(self, student: Student) -> list[Attendance]:
        query = (
            "SELECT student_id, lesson_id AS id, st.group_id, l.name, start_time, visit_status"
            " FROM students AS st "
            " JOIN attendances AS at ON st.telegram_id = at.student_id "
            " JOIN lessons as l ON at.lesson_id = l.id"
            " WHERE student_id = $1 "
        )
        records: list[Mapping] = await self._con.fetch(query, student.telegram_id)

        attendances = [Attendance.from_mapping(record) for record in records]
        attendances.sort()

        return attendances

    async def get_visit_status_for_group_students(self, group_id: int, lesson: Lesson) -> dict[Student, VisitStatus]:
        query = (
            "SELECT "
            "st.telegram_id, st.name, st.surname, st.group_id, st.is_headman, st.university_id,"
            " visit_status "
            " FROM students AS st "
            " JOIN attendances AS at ON st.telegram_id = at.student_id "
            " WHERE st.group_id = $1 AND at.lesson_id = $2"
        )

        records: list[Mapping] = await self._con.fetch(query, group_id, lesson.id)

        return {Student.from_mapping(record): record["visit_status"] for record in records}

    async def get_visit_status_by_student_and_lesson(self, student: Student, lesson: Lesson) -> VisitStatus:
        query = "SELECT visit_status FROM attendances WHERE student_id = $1 AND lesson_id = $2"
        status = await self._con.fetchval(query, student.telegram_id, lesson.id)
        return VisitStatus(status)

    async def update_visit_status_by_student(self, student: Student, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2"
        await self._con.execute(query, new_status, student.telegram_id)

    async def update_visit_status(self, student: Student, lesson_id: int, new_status: VisitStatus) -> None:
        attendances = await self.filter_by_student(student)

        for attendance in attendances:
            if attendance.status == VisitStatus.NOT_CHECKED:
                await self._update_status(student.telegram_id, attendance.lesson.id, VisitStatus.NOT_VISIT)

        await self._update_status(student.telegram_id, lesson_id, new_status)

        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2 AND lesson_id = $3"
        await self._con.execute(query, new_status, student.telegram_id, lesson_id)

    async def _update_status(self, student_id: int, lesson_id: int, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2 AND lesson_id = $3"
        await self._con.execute(query, new_status, student_id, lesson_id)

    async def _delete_all_attendances(self) -> None:
        query = "TRUNCATE TABLE attendances"
        await self._con.execute(query)

    async def _create(self, student: Student) -> None:
        lesson_service = LessonService(self._con)
        lessons = await lesson_service.filter_by_student(student)

        if lessons is None:
            return

        query = "INSERT INTO attendances VALUES($1, $2, $3)"

        await self._con.executemany(
            query, ((student.telegram_id, lesson.id, VisitStatus.NOT_CHECKED) for lesson in lessons)
        )
