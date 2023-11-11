from dataclasses import dataclass
from typing import Mapping, Self

from src.dto import Attendance, Student
from src.dto.dto import DTO

__all__ = [
    "GroupAttendances",
]


@dataclass(slots=True)
class GroupAttendances(DTO):
    group_id: int
    attendances: dict[int, list[Attendance]]

    def get_attendances_by_student(self, student: Student) -> list[Attendance]:
        return self.attendances[student.telegram_id]

    @classmethod
    def from_mapping(cls, _: Mapping) -> Self:
        raise NotImplementedError
