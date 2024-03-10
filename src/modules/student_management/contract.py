from abc import ABC, abstractmethod
from typing import Any

__all__ = [
    "StudentManagementContract",
]


class StudentManagementContract(ABC):
    @abstractmethod
    async def get_students_info(self, group_id: int) -> list[dict[str, Any]]:
        """Return data in format like.

        student_info = return_value[0]

        student_info['id']: int -> student id
        student_info['telegram_id']: int -> student telegram id
        student_info['first_name']: str -> student name
        student_info['last_name']: str -> student surname
        student_info['attendance_noted']: bool -> True mean, that student already have checked in today.
        """

    @abstractmethod
    async def get_headman_by_group_id(self, group_id: int) -> dict:
        ...

    @abstractmethod
    async def note_student_attendance(self, student_id: int) -> None:
        ...
