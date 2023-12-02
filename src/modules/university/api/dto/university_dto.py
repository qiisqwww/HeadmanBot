from dataclasses import dataclass

from src.kernel.base import DTO
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "UniversityDTO",
]


@dataclass(slots=True, frozen=True)
class UniversityDTO(DTO):
    id: int
    name: str
    alias: UniversityAlias
