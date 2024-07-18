from dataclasses import dataclass

from src.modules.common.domain import UniversityAlias
from src.modules.student_management.domain import Role

__all__ = [
    "StudentEnterGroupDTO",
]


@dataclass(slots=True, frozen=True)
class StudentEnterGroupDTO:
    telegram_id: int
    role: Role
    group_name: str
    university_alias: UniversityAlias
