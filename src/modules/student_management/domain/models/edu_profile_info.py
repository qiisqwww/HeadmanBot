from dataclasses import dataclass

__all__ = [
    "EduProfileInfo",
]


@dataclass(slots=True, frozen=True)
class EduProfileInfo:
    group_name: str | None
    university_name: str | None
