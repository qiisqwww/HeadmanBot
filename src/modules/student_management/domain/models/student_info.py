from dataclasses import dataclass

__all__ = [
    "StudentInfo",
]


@dataclass(slots=True, frozen=True)
class StudentInfo:
    id: int
    telegram_id: int
    first_name: str
    last_name: str
    attendance_noted: bool

    @property
    def fullname(self) -> str:
        return f"{self.last_name} {self.first_name}"
