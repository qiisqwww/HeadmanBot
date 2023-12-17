from dataclasses import dataclass
from typing import NewType

from .dto import DTO
from .university import UniversityId

__all__ = [
    "Group",
    "GroupId",
]

GroupId = NewType("GroupId", int)


@dataclass(slots=True, frozen=True)
class Group(DTO):
    id: GroupId
    name: str
    university_id: UniversityId
