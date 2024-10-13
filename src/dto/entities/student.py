from dataclasses import dataclass
from datetime import date
from typing import NewType, Self, Any, Mapping

from src.dto.enums import Role
from .group import GroupId

__all__ = [
    "Student",
    "StudentId",
]

StudentId = NewType("StudentId", int)


@dataclass(slots=True, frozen=True)
class Student:
    id: StudentId
    telegram_id: int
    group_id: GroupId
    first_name: str
    last_name: str
    username: str | None
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

    @property
    def fullname(self) -> str:
        return f"{self.last_name} {self.first_name}"

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Self:
        return cls(
            id=StudentId(record["id"]),
            telegram_id=record["telegram_id"],
            first_name=record["first_name"],
            last_name=record["last_name"],
            group_id=GroupId(record["group_id"]),
            role=Role(record["role"]),
            birthdate=record["birthdate"],
            attendance_noted=record["attendance_noted"],
            username=record["username"],
        )
