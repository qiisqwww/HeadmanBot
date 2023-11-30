from dataclasses import dataclass
from typing import Mapping, Self

from src.modules.student.internal.enums import Role
from src.modules.university.api.enums import UniversityAlias

__all__ = [
    "StudentRaw",
]


@dataclass(slots=True, frozen=True)
class StudentRaw:
    telegram_id: int
    name: str
    surname: str
    birthday: int | None
    birthmonth: int | None
    role: Role
    university_alias: UniversityAlias
    group_name: str

    @classmethod
    def from_mapping(cls, data: Mapping[str, str]) -> Self:
        return cls(
            telegram_id=int(data["telegram_id"]),
            name=data["name"],
            surname=data["surname"],
            birthday=None if data["birthday"] == "0" else int(data["birthday"]),
            birthmonth=None if data["birthmonth"] == "0" else int(data["birthmonth"]),
            role=Role(data["role"]),
            university_alias=UniversityAlias(data["university_alias"]),
            group_name=data["group_name"],
        )
