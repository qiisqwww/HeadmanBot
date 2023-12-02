from dataclasses import dataclass

from src.kernel.base import DTO

__all__ = [
    "GroupDTO",
]


@dataclass(slots=True, frozen=True)
class GroupDTO(DTO):
    id: int
    name: str
    university_id: int
