from dataclasses import dataclass
from typing import NewType

from src.kernel.base import DTO
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "UniversityDTO",
    "UniversityId",
]

UniversityId = NewType("UniversityId", int)


@dataclass(slots=True, frozen=True)
class UniversityDTO(DTO):
    id: UniversityId
    name: str
    alias: UniversityAlias
