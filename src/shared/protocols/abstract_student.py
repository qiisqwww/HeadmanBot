from typing import Protocol


class AbstractStudent(Protocol):
    @property
    def telegram_id(self) -> int:
        ...
