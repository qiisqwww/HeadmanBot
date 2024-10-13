from enum import UNIQUE, Enum, verify

__all__ = [
    "VisitStatus",
]


@verify(UNIQUE)
class VisitStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
