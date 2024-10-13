from datetime import date
from typing import final

from src.common.repositories import PostgresRepository
from src.dto.entities import Attendance, Lesson, StudentId, AttendanceId
from src.dto.enums import VisitStatus

__all__ = [
    "AttendanceRepository",
]


@final
class AttendanceRepository(PostgresRepository):
    async def create_for_student(self, student_id: StudentId, schedule: list[Lesson], day: date) -> None:
        query = "INSERT INTO attendances (student_id, lesson_id, status, date) VALUES($1, $2, $3, $4)"
        await self._con.executemany(
            query,
            ((student_id, lesson.id, VisitStatus.ABSENT, day) for lesson in schedule),
        )

    async def filter_by_student_id(self, student_id: StudentId) -> list[Attendance]:
        query = """SELECT at.id, at.lesson_id, at.status, le.group_id, le.name, le.start_time
                   FROM attendances AS at
                   JOIN lessons AS le
                   ON at.lesson_id = le.id
                   WHERE student_id = $1 AND NOT at.archived AND not le.archived
                   ORDER BY le.start_time
                   """

        records = await self._con.fetch(query, student_id)

        return [Attendance.from_record(record, student_id=student_id) for record in records]

    async def update_status(self, attendance_id: AttendanceId, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET status = $1 WHERE id = $2"
        await self._con.execute(query, new_status, attendance_id)

    async def update_status_for_student(self, student_id: StudentId, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET status = $1 WHERE student_id = $2"
        await self._con.execute(query, new_status, student_id)

    async def delete_attendance_by_student_id(self, student_id: int) -> None:
        query = "UPDATE attendances SET archived=TRUE WHERE student_id = $1"
        await self._con.execute(query, student_id)

    async def delete_attendance_by_group_id(self, group_id: int) -> None:
        query = """UPDATE attendances 
                   SET archived=TRUE
                   WHERE lesson_id
                   IN (
                       SELECT id FROM lessons WHERE group_id = $1 AND NOT archived
                    )"""
        await self._con.execute(query, group_id)
