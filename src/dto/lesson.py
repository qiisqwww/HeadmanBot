from dataclasses import dataclass
from datetime import time

from asyncpg import Record

__all__ = [
    "Lesson",
]


@dataclass(frozen=True, slots=True)
class Lesson:
    id: int
    group_id: int
    discipline: str
    start_time: time
    weekday: int

    @classmethod
    def from_record(cls, record: Record) -> "Lesson":
        return Lesson(**dict(record))
