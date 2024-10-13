from dataclasses import dataclass
from typing import Mapping, Self

from src.dto.enums import UniversityAlias, Role

__all__ = [
    "StudentEnterGroupDTO",
]


@dataclass(slots=True, frozen=True)
class StudentEnterGroupDTO:
    telegram_id: int
    role: Role
    group_name: str
    university_alias: UniversityAlias

    def to_redis_dict(self) -> Mapping[bytes | str, str]:
        return {
            "role": self.role.value,
            "group_name": self.group_name,
            "telegram_id": str(self.telegram_id),
            "university_alias": self.university_alias.value,
        }

    @classmethod
    def from_redis_dict(cls, data: Mapping[str, str]) -> Self:
        return cls(
            role=Role(data["role"]),
            group_name=data["group_name"],
            telegram_id=int(data["telegram_id"]),
            university_alias=UniversityAlias(data["university_alias"]),
        )
