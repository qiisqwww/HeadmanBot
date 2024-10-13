from dataclasses import dataclass
from typing import NewType, Mapping, Any, Self

from src.dto.enums import UniversityAlias
from .university import UniversityId, University

__all__ = [
    "Group",
    "GroupId",
]

GroupId = NewType("GroupId", int)


@dataclass(slots=True, frozen=True)
class Group:
    id: GroupId
    name: str
    university: University

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Self:
        return cls(
            id=GroupId(record["id"]),
            name=record["name"],
            university=University(
                id=UniversityId(record["university_id"]),
                name=record["university_name"],
                alias=UniversityAlias(record["university_alias"]),
                timezone=record["university_timezone"],
            ),
        )
