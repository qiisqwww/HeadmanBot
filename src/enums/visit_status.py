from enum import (
    UNIQUE,
    Enum,
    verify
)

__all__ = [
    "VisitStatus",
]


@verify(UNIQUE)
class VisitStatus(str, Enum):
    VISIT = "visit"
    NOT_VISIT = "not visit"
    NOT_CHECKED = "not checked"
