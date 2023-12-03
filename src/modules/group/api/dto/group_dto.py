from dataclasses import dataclass

from src.kernel.base import DTO
from src.kernel.student_dto import GroupId
from src.modules.university.api.dto import UniversityId

__all__ = [
    "GroupDTO",
]


@dataclass(slots=True, frozen=True)
class GroupDTO(DTO):
    id: GroupId
    name: str
    university_id: UniversityId
