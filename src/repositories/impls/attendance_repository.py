from src.dto.models import (
    AttendanceWithLesson,
    GroupId,
    Lesson,
    LessonId,
    StudentId,
    StudentReadFullname,
)
from src.enums import VisitStatus

from ..interfaces import AttendanceRepository
from .postgres_repository import PostgresRepositoryImpl

__all__ = [
    "AttendanceRepositoryImpl",
]


class AttendanceRepositoryImpl(PostgresRepositoryImpl, AttendanceRepository):
    async def get_visit_status_by_student_id_and_lesson(
        self, student_id: StudentId, lesson_id: LessonId
    ) -> VisitStatus:
        query = "SELECT visit_status FROM attendances WHERE student_id = $1 AND lesson_id = $2"
        status = await self._con.fetchval(query, student_id, lesson_id)
        return VisitStatus(status)

    async def update_visit_status_all(self, student_id: StudentId, new_status: VisitStatus) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2"
        await self._con.execute(query, new_status, student_id)

    async def update_status_for_lesson(
        self, student_id: StudentId, lesson_id: LessonId, new_status: VisitStatus
    ) -> None:
        query = "UPDATE attendances SET visit_status = $1 WHERE student_id = $2 AND lesson_id = $3"
        await self._con.execute(query, new_status, student_id, lesson_id)

    async def delete_all_attendances(self) -> None:
        query = "TRUNCATE TABLE attendances"
        await self._con.execute(query)

    async def create(self, student_id: StudentId, lesson_ids: list[LessonId]) -> None:
        query = "INSERT INTO attendances VALUES($1, $2, $3)"
        await self._con.executemany(
            query, ((student_id, lesson_id, VisitStatus.NOT_CHECKED) for lesson_id in lesson_ids)
        )

    async def filter_by_student_id(self, student_id: StudentId) -> list[AttendanceWithLesson]:
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

    async def get_visit_status_for_group_students(
        self, group_id: GroupId, lesson_id: LessonId
    ) -> dict[StudentReadFullname, VisitStatus]:
        query = (
            "SELECT "
            "st.telegram_id, st.name, st.surname, at.visit_status"
            " FROM attendances AS at "
            " JOIN students AS st "
            " ON st.telegram_id = at.student_id "
            " WHERE at.lesson_id = $1 AND st.group_id = $2 "
        )

        records = await self._con.fetch(query, lesson_id, group_id)

        return {StudentReadFullname.from_mapping(record): VisitStatus(record["visit_status"]) for record in records}
