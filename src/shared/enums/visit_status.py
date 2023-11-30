from enum import Enum

__all__ = [
    "VisitStatus",
]


class VisitStatus(str, Enum):
    VISIT = "visit"
    NOT_VISIT = "not visit"
    NOT_CHECKED = "not checked"
