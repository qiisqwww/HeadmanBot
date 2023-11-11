from typing import Any, Mapping

from src.dto import Attendance
from src.dto.group_attendances import GroupAttendances

from .base import Repository

__all__ = [
    "AttendaceRepository",
]


class AttendaceRepository(Repository):
    async def get_by_pk(self, student_id: int, lesson_id: int) -> Attendance | None:
        query = (
            "SELECT * FROM attendance "
            "JOIN lessons AS le ON lesson_id = le.id "
            "WHERE lesson_id = $1 and student_id = $2"
        )
        record = await self._con.fetchrow(query, lesson_id, student_id)

        if record is None:
            return None

        return Attendance.from_mapping(record)

    async def all(self) -> list[Attendance]:
        query = "SELECT * FROM attendance JOIN lessons AS le ON lesson_id = le.id "
        records = await self._con.fetch(query)

        return [Attendance.from_mapping(record) for record in records]

    async def create(self, data: Mapping) -> Attendance:
        query = "INSERT INTO attendance (lesson_id, student_id, status) VALUES ($1, $2, $3 ) RETURNING"
        await self._con.execute(query, data["lesson"].id, data["student_id"], data["status"])

        return Attendance.from_mapping(data)

    async def update(self, dto: Attendance) -> Attendance:
        query = "UPDATE SET lesson_id=$1, student_id=$2, visit_status=$3 WHERE lesson_id=$4, student_id=$5"
        await self._con.execute(query, dto.lesson.id, dto.student_id, dto.status, dto.lesson.id, dto.student_id)
        return dto

    async def patch(self, dto: Attendance, column: str, new_value: Any) -> Attendance:
        query = "UPDATE attendance SET $1=$2 WHERE lesson_id = $3 AND student_id = $4"
        await self._con.execute(query, column, new_value, dto.lesson.id, dto.student_id)
        setattr(dto, column, new_value)
        return dto

    async def delete(self, dto: Attendance) -> None:
        query = "DELETE FROM attendance WHERE lesson_id = $1 AND student_id = $2"
        await self._con.execute(query, dto.lesson.id, dto.student_id)

    async def filter_by_student(self, student_id: int) -> list[Attendance]:
        query = (
            "SELECT student_id, lesson_id AS id, st.group_id, discipline, start_time, weekday, visit_status"
            " FROM students AS st "
            " JOIN attendance AS at ON st.telegram_id = at.student_id "
            " JOIN lessons as l ON at.lesson_id = l.id"
            " WHERE student_id = $1 "
        )
        records: list[Mapping] = await self._con.fetch(query, student_id)

        attendances = [Attendance.from_mapping(record) for record in records]
        attendances.sort()

        return attendances

    async def get_group_attendances(self, group_id: int) -> GroupAttendances:
        query = (
            "SELECT student_id, lesson_id AS id, st.group_id, discipline, start_time, weekday, visit_status"
            " FROM students AS st "
            " JOIN attendance AS at ON st.telegram_id = at.student_id "
            " JOIN lessons as l ON at.lesson_id = l.id "
            " WHERE st.group_id = $1 "
        )

        records: list[Mapping] = await self._con.fetch(query, group_id)
        attendances_data: dict[int, list[Attendance]] = {}

        for record in records:
            student_id = record["student_id"]

            new_attendance = Attendance.from_mapping(record)

            if student_id not in attendances_data:
                attendances_data[student_id] = [new_attendance]
            else:
                attendances_data[student_id].append(new_attendance)

        return GroupAttendances(
            group_id=group_id,
            attendances=attendances_data,
        )
