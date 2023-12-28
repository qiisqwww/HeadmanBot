from dataclasses import dataclass
from datetime import date

from src.enums import Role, UniversityAlias

from .model import Model

__all__ = [
    "StudentLoginData",
]


@dataclass(slots=True, frozen=True)
class StudentLoginData(Model):
    telegram_id: int
    name: str
    surname: str
    birthdate: date | None
    role: Role
    university_alias: UniversityAlias
    group_name: str
