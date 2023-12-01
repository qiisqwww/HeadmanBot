from abc import ABC

__all__ = [
    "AbstractStudent",
]


class AbstractStudent(ABC):
    telegram_id: int
    name: str
    surname: str
    birthday: int | None
    birthmonth: int | None
