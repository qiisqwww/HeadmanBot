from dataclasses import dataclass

from asyncpg import Record

__all__ = [
    "University",
]


@dataclass
class University:
    id: int
    name: str

    @classmethod
    def from_record(cls, record: Record) -> "University":
        return University(**dict(record))
