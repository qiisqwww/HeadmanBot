from dataclasses import dataclass
from typing import NewType

from src.enums import UniversityAlias

from .dto import DTO

__all__ = [
    "University",
    "UniversityId",
]

UniversityId = NewType("UniversityId", int)


@dataclass(slots=True, frozen=True)
class University(DTO):
    id: UniversityId
    name: str
    alias: UniversityAlias
