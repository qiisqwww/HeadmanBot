from dataclasses import dataclass
from datetime import date
from typing import NewType

from src.enums import Role

from .group import Group
from .model import Model

__all__ = [
    "Student",
    "StudentId",
]

StudentId = NewType("StudentId", int)


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class Student(Model):
    telegram_id: StudentId
    group: Group
    name: str
    surname: str
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
