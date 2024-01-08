from dataclasses import dataclass
from datetime import date

from ..enums import Role

__all__ = [
    "Student",
]


@dataclass(slots=True, frozen=True)
class Student:
    id: int
    telegram_id: int
    group_id: int
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

    def __hash__(self) -> int:
        return hash(self.id)
