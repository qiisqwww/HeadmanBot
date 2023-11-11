from dataclasses import dataclass
from typing import Mapping, Self

from src.dto.dto import DTO

__all__ = [
    "Group",
]


@dataclass(slots=True)
class Group(DTO):
    id: int
    name: str

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
        )
