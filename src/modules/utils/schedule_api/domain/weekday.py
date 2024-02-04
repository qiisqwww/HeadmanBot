from datetime import UTC, datetime
from enum import CONTINUOUS, UNIQUE, IntEnum, verify
from typing import Self

__all__ = [
    "Weekday",
]


@verify(UNIQUE, CONTINUOUS)
class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @classmethod
    def today(cls: type[Self]) -> Self:
        return cls(datetime.now(tz=UTC).weekday())
