from enum import CONTINUOUS, UNIQUE, IntEnum, verify

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
