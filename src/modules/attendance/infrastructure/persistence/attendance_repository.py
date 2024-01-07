from src.dto.models import StudentId
from src.repositories.exceptions import CorruptedDatabaseError
from src.repositories.impls.postgres_repository import PostgresRepositoryImpl

from ...domain.enums import VisitStatus
from ...domain.models import Attendance, AttendanceId, Lesson
from ...domain.repositories import AttendanceRepository

__all__ = [
    "AttendanceRepositoryImpl",
]


class AttendanceRepositoryImpl(PostgresRepositoryImpl, AttendanceRepository):
    async def create_for_student(self, student_id: StudentId) -> None:
        """Create all attendances for this student and its lessons."""
        query = "INSERT INTO attendances VALUES($1, $2, $3)"
        await self._con.executemany(
            query, ((student_id, lesson_id, VisitStatus.NOT_CHECKED) for lesson_id in lesson_ids)
        )

    async def filter_by_student_id(self, student_id: StudentId) -> list[Attendance]:
        query = "SELECT * FROM attendances AS at JOIN lessons AS le ON at.lesson_id = le.id  WHERE student_id = $1"

        records = await self._con.fetch(query, student_id)

        return [
            AttendanceWithLesson(
                student_id=student_id,
                status=VisitStatus(record["visit_status"]),
                lesson=Lesson.from_mapping(record),
            )
            for record in records
        ]

    async def find_or_fail(self, attendance_id: AttendanceId) -> Attendance:
        query = "SELECT * FROM attendances WHERE id = $1"
        record = await self._con.fetchrow(query, attendance_id)

        if record is None:
            raise CorruptedDatabaseError

        return Attendance.from_mapping(record)

    async def update_status(self, attendance_id: AttendanceId, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE id = $2"
        await self._con.execute(query, new_status, attendance_id)

    @abstractmethod
    async def update_status_for_student(self, student_id: StudentId, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2"
        await self._con.execute(query, new_status, student_id)

    async def delete_all(self) -> None:
        query = "TRUNCATE TABLE attendances"
        await self._con.execute(query)
