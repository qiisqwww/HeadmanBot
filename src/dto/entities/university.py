from dataclasses import dataclass
from typing import NewType, Self, Any, Mapping

from src.dto.enums import UniversityAlias

__all__ = [
    "University",
    "UniversityId",
]

UniversityId = NewType("UniversityId", int)


@dataclass(slots=True, frozen=True)
class University:
    id: UniversityId
    name: str
    alias: UniversityAlias
    timezone: str

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Self:
        return cls(
            id=UniversityId(record["id"]),
            name=record["name"],
            alias=UniversityAlias(record["alias"]),
            timezone=record["timezone"],
        )
