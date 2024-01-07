from dataclasses import dataclass

from src.modules.common.domain import UniversityAlias

__all__ = [
    "UniversityInfo",
]


@dataclass(slots=True, frozen=True)
class UniversityInfo:
    id: int
    name: str
    alias: UniversityAlias
