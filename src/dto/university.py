from dataclasses import dataclass
from typing import Mapping, Self

from src.enums import UniversityAlias

__all__ = [
    "University",
]


@dataclass(slots=True)
class University:
    id: int
    name: str
    alias: UniversityAlias

    @classmethod
    def from_mapping(cls, data: Mapping) -> Self:
        return cls(
            id=data["id"],
            name=data["name"],
            alias=UniversityAlias(data["alias"]),
        )
