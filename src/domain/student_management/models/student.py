from dataclasses import dataclass
from datetime import date
from typing import NewType

from src.domain.common import Model

from ..enums import Role
from .group import Group

__all__ = [
    "Student",
    "StudentId",
]

StudentId = NewType("StudentId", int)


@dataclass(slots=True, frozen=True, unsafe_hash=True)
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
