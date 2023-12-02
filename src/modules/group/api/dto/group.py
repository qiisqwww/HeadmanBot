from dataclasses import dataclass
from typing import Mapping, Self

__all__ = [
    "Group",
]


@dataclass(slots=True, frozen=True)
class Group:
    id: int
    headman_id: int
    university_id: int
    name: str

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
            headman_id=data["headman_id"],
            university_id=data["university_id"],
        )