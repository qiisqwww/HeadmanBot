from dataclasses import dataclass

__all__ = [
    "EduProfileInfo",
]


@dataclass(slots=True, frozen=True)
class EduProfileInfo:
    group_name: str
    university_name: str
