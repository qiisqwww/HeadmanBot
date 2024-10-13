from dataclasses import dataclass
from datetime import date
from typing import Mapping, Self

from src.dto.enums import UniversityAlias, Role

__all__ = [
    "CreateStudentDTO",
]


@dataclass(slots=True, frozen=True)
class CreateStudentDTO:
    telegram_id: int
    first_name: str
    last_name: str
    username: str | None
    birthdate: date | None
    role: Role
    group_name: str
    university_alias: UniversityAlias

    def to_redis_dict(self) -> Mapping[bytes | str, str]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.value,
            "group_name": self.group_name,
            "telegram_id": str(self.telegram_id),
            "university_alias": self.university_alias.value,
            "birthdate": "0" if self.birthdate is None else self.birthdate,
            "username": "" if self.username is None else self.username,
        }

    @classmethod
    def from_redis_dict(cls, data: Mapping[str, str]) -> Self:
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=Role(data["role"]),
            group_name=data["group_name"],
            telegram_id=int(data["telegram_id"]),
            university_alias=UniversityAlias(data["university_alias"]),
            birthdate=None if data["birthdate"] == "0" else date.fromisoformat(data["birthdate"]),
            username=None if data["username"] == "" else data["username"],
        )
