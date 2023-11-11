from dataclasses import dataclass
from typing import Mapping, Self

from .dto import DTO

__all__ = [
    "University",
]


@dataclass(slots=True)
class University(DTO):
    id: int
    name: str

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
        )
