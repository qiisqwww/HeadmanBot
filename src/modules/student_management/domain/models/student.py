from dataclasses import dataclass
from datetime import date

from src.modules.student_management.domain import Role

__all__ = [
    "Student",
]


@dataclass(slots=True, frozen=True)
class Student:
    id: int
    telegram_id: int
    group_id: int
    first_name: str
    last_name: str
    role: Role
    birthdate: date | None
    attendance_noted: bool

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    def is_headman(self) -> bool:
        return self.role == Role.HEADMAN

    def is_vice_headman(self) -> bool:
        return self.role == Role.VICE_HEADMAN

    def is_student(self) -> bool:
        return self.role == Role.STUDENT

    def __hash__(self) -> int:
        return hash(self.id)
