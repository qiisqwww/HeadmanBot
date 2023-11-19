from dataclasses import dataclass
from typing import Mapping, Self

from .dto import DTO

__all__ = [
    "Student",
]


@dataclass(slots=True, unsafe_hash=True)
class Student(DTO):
    telegram_id: int
    group_id: int
    university_id: int
    name: str
    surname: str
    is_headman: bool

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            telegram_id=data["telegram_id"],
            group_id=data["group_id"],
            university_id=data["university_id"],
            name=data["name"],
            surname=data["surname"],
            is_headman=data["is_headman"],
        )

    @property
    def telegram_link(self) -> str:
        return f'<a href="tg://user?id={self.telegram_id}">{self.surname} {self.name}</a>\n'

    @property
    def fullname(self) -> str:
        return f"{self.surname} {self.name}"
