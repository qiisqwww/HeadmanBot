from dataclasses import dataclass

from .base.dto import DTO
from .role import Role

__all__ = [
    "StudentDTO",
]


@dataclass(slots=True, frozen=True, unsafe_hash=True)
class StudentDTO(DTO):
    telegram_id: int
    name: str
    surname: str
    role: Role

    @property
    def telegram_link(self) -> str:
        return f'<a href="tg://user?id={self.telegram_id}">{self.surname} {self.name}</a>\n'

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
