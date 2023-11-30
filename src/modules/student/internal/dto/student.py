from dataclasses import dataclass
from typing import Mapping, Self

from src.shared.abstract_dto import AbstractStudent

__all__ = [
    "Student",
]


@dataclass(slots=True, unsafe_hash=True, frozen=True)
class Student(AbstractStudent):
    telegram_id: int
    name: str
    surname: str
    birthday: int | None
    birthmonth: int | None

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            telegram_id=data["telegram_id"],
            name=data["name"],
            surname=data["surname"],
            birthday=data["birthday"],
            birthmonth=data["birthmonth"],
        )

    @property
    def telegram_link(self) -> str:
        return f'<a href="tg://user?id={self.telegram_id}">{self.surname} {self.name}</a>\n'

    @property
    def fullname(self) -> str:
        return f"{self.surname} {self.name}"
