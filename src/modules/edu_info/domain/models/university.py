from dataclasses import dataclass

from src.modules.common.domain import UniversityAlias

__all__ = [
    "University",
]


@dataclass(slots=True, frozen=True)
class University:
    id: int
    name: str
    alias: UniversityAlias
