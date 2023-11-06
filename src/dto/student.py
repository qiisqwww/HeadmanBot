from dataclasses import dataclass

from asyncpg import Record

__all__ = [
    "Student",
]


@dataclass(slots=True)
class Student:
    telegram_id: int
    group_id: int
    university_id: int
    name: str
    surname: str
    telegram_name: str | None
    is_headman: bool

    @classmethod
    def from_record(cls, record: Record) -> "Student":
        return Student(**dict(record))
