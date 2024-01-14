from dataclasses import dataclass

__all__ = [
    "StudentInfo",
]


@dataclass(slots=True, frozen=True)
class StudentInfo:
    id: int
    telegram_id: int
    name: str
    surname: str
    is_checked_in_today: bool
