from dataclasses import dataclass
from datetime import date
from typing import NewType

from src.domain.common import Model
from src.domain.edu_info.models import Group

from ..enums import Role

__all__ = [
    "Student",
    "StudentId",
]

StudentId = NewType("StudentId", int)


@dataclass(slots=True)
class Student(Model):
    telegram_id: StudentId
    name: str
    surname: str
    group: Group
    role: Role
    birthdate: date | None
    is_checked_in_today: bool

    @property
    def fullname(self) -> str:
        return f"{self.surname} {self.name}"

    def is_headman(self) -> bool:
        return self.role == Role.HEADMAN

    def is_admin(self) -> bool:
        return self.role == Role.ADMIN

    def is_vice_headman(self) -> bool:
        return self.role == Role.VICE_HEADMAN

    def is_student(self) -> bool:
        return self.role == Role.STUDENT

    def __hash__(self) -> int:
        return hash(self.telegram_id)
