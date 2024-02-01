from dataclasses import dataclass

from src.modules.common.domain import UniversityAlias

__all__ = [
    "GroupInfo",
]


@dataclass(slots=True, frozen=True)
class GroupInfo:
    id: int 
    name: str
    alias: UniversityAlias
