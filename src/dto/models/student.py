from dataclasses import dataclass
from datetime import date
from typing import NewType

from src.enums import Role

from .dto import DTO
from .group import GroupId

__all__ = [
    "Student",
    "StudentId",
]

StudentId = NewType("StudentId", int)


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class Student(DTO):
    telegram_id: StudentId
    group_id: GroupId
    name: str
    surname: str
    role: Role
    birthdate: date | None

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