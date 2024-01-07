from dataclasses import dataclass

__all__ = [
    "Group",
]


@dataclass(slots=True, frozen=True)
class Group:
    id: int
    name: str
    university_id: int
