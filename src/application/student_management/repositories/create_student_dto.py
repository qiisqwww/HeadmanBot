from dataclasses import dataclass
from datetime import date

from src.domain.edu_info import UniversityAlias
from src.domain.student_management import Role

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
    university_alias: UniversityAlias
    group_name: str
