from dataclasses import dataclass
from datetime import date

from src.modules.common.domain import UniversityAlias
from src.modules.student_management.domain import Role

__all__ = [
    "CreateStudentDTO",
]


@dataclass(slots=True, frozen=True)
class CreateStudentDTO:
    telegram_id: int
    name: str
    surname: str
    birthdate: date | None
    role: Role
    group_name: str
    university_alias: UniversityAlias
