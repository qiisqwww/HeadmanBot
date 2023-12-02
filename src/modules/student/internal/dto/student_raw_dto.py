from dataclasses import dataclass
from datetime import date

from src.kernel.base import DTO
from src.kernel.role import Role
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "StudentRawDTO",
]


@dataclass(slots=True, frozen=True)
class StudentRawDTO(DTO):
    telegram_id: int
    name: str
    surname: str
    birthdate: date | None
    role: Role
    university_alias: UniversityAlias
    group_name: str
