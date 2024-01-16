from typing import final

from src.modules.attendance.application.repositories import AttendanceRepository
from src.modules.attendance.domain import Attendance, Lesson, VisitStatus
from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl

__all__ = [
    "AttendanceRepositoryImpl",
]


@final
class AttendanceRepositoryImpl(PostgresRepositoryImpl, AttendanceRepository):
    async def create_for_student(self, student_id: int, schedule: list[Lesson]) -> None:
        query = "INSERT INTO attendance.attendances (student_id, lesson_id, status) VALUES($1, $2, $3)"
        await self._con.executemany(query, ((student_id, lesson.id, VisitStatus.ABSENT) for lesson in schedule))

    async def filter_by_student_id(self, student_id: int) -> list[Attendance]:
        query = """SELECT at.id, at.lesson_id, at.status, le.group_id, le.name, le.start_time
                   FROM attendance.attendances AS at 
                   JOIN attendance.lessons AS le 
                   ON at.lesson_id = le.id  
                   WHERE student_id = $1"""

        records = await self._con.fetch(query, student_id)

        return [
            Attendance(
                id=record["id"],
                student_id=student_id,
                status=VisitStatus(record["status"]),
                lesson=Lesson(
                    id=record["lesson_id"],
                    group_id=record["group_id"],
                    start_time=record["start_time"],
                    name=record["name"],
                ),
            )
            for record in records
        ]

    async def update_status(self, attendance_id: int, new_status: VisitStatus) -> None:
        query = "UPDATE attendance.attendances SET status = $1 WHERE id = $2"
        await self._con.execute(query, new_status, attendance_id)

    async def update_status_for_student(self, student_id: int, new_status: VisitStatus) -> None:
        query = "UPDATE attendance.attendances SET status = $1 WHERE student_id = $2"
        await self._con.execute(query, new_status, student_id)

    # async def delete_all(self) -> None:
    #     query = "TRUNCATE TABLE attendances"
    #     await self._con.execute(query)
