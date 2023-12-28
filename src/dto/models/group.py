from dataclasses import dataclass
from typing import NewType

from .model import Model
from .university import UniversityId

__all__ = [
    "Group",
    "GroupId",
]

GroupId = NewType("GroupId", int)


@dataclass(slots=True, frozen=True)
class Group(Model):
    id: GroupId
    name: str
    university_id: UniversityId
