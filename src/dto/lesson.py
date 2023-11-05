from dataclasses import dataclass

__all__ = [
    "Lesson",
]


@dataclass(frozen=True, slots=True)
class Lesson:
    discipline: str
    start_time: str  # In format like "10:00"

    def __str__(self) -> str:
        return f"{self.discipline}|{self.start_time}"

    @classmethod
    def from_str(cls, string: str) -> "Lesson":
        return Lesson(*string.split("|"))
