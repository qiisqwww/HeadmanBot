from dataclasses import dataclass
from datetime import date

from src.enums import Role, UniversityAlias

from .dto import DTO

__all__ = [
    "StudentLoginData",
]


@dataclass(slots=True, frozen=True)
class StudentLoginData(DTO):
    telegram_id: int
    name: str
    surname: str
    birthdate: date | None
    role: Role
    university_alias: UniversityAlias
    group_name: str
