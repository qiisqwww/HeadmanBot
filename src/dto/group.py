from dataclasses import dataclass

from asyncpg import Record

__all__ = [
    "Group",
]


@dataclass(slots=True)
class Group:
    id: int
    name: str

    @classmethod
    def from_record(cls, record: Record) -> "Group":
        return Group(**dict(record))
