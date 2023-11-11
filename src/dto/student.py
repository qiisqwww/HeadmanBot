from dataclasses import dataclass
from typing import Mapping, Self

from .dto import DTO

__all__ = [
    "Student",
]


@dataclass(slots=True)
class Student(DTO):
    telegram_id: int
    group_id: int
    university_id: int
    name: str
    surname: str
    telegram_name: str | None
    is_headman: bool

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            telegram_id=data["telegram_id"],
            group_id=data["group_id"],
            university_id=data["university_id"],
            name=data["name"],
            surname=data["surname"],
            telegram_name=data["telegram_name"],
            is_headman=data["is_headman"],
        )
