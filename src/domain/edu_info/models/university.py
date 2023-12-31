from dataclasses import dataclass
from typing import NewType

from src.domain.common import Model

from ..enums import UniversityAlias

__all__ = [
    "University",
    "UniversityId",
]

UniversityId = NewType("UniversityId", int)


@dataclass(slots=True, frozen=True)
class University(Model):
    id: UniversityId
    name: str
    alias: UniversityAlias