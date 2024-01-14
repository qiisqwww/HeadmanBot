from typing import final

from src.modules.attendance.application.repositories import GroupAttendanceRepository
from src.modules.attendance.domain import (
    LessonAttendanceForGroup,
    StudentInfo,
    VisitStatus,
)
from src.modules.common.infrastructure.persistence import PostgresRepositoryImpl


@final
class GroupAttendanceRepositoryImpl(PostgresRepositoryImpl, GroupAttendanceRepository):
    async def find_group_visit_status_for_lesson(
        self, group_id: int, lesson_id: int, students_info: dict[int, StudentInfo]
    ) -> LessonAttendanceForGroup:
        query = """
        SELECT status, student_id
        FROM attendance.attendances
        WHERE lesson_id = $1
        """

        records = await self._con.fetch(query, lesson_id)

        return LessonAttendanceForGroup(
            group_id=group_id,
            lesson_id=lesson_id,
            attendance={
                VisitStatus.ABSENT: [
                    students_info[record["student_id"]] for record in records if record["status"] == VisitStatus.ABSENT
                ],
                VisitStatus.PRESENT: [
                    students_info[record["student_id"]] for record in records if record["status"] == VisitStatus.PRESENT
                ],
            },
        )
