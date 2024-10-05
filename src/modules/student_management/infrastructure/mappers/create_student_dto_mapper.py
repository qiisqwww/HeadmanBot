from collections.abc import Mapping
from datetime import date
from typing import final

from src.modules.common.domain import UniversityAlias
from src.modules.student_management.application.repositories import CreateStudentDTO
from src.modules.student_management.domain import Role

__all__ = [
    "CreateStudentDTOMapper",
]


@final
class CreateStudentDTOMapper:
    def to_redis_dict(self, data: CreateStudentDTO) -> Mapping[bytes | str, str]:
        return {
            "first_name": data.first_name,
            "last_name": data.last_name,
            "role":  data.role.value,
            "group_name": data.group_name,
            "telegram_id":  str(data.telegram_id),
            "university_alias": data.university_alias.value,
            "birthdate": "0" if data.birthdate is None else data.birthdate,
        }

    def from_redis_dict(self, data: Mapping[str, str]) -> CreateStudentDTO:
        return CreateStudentDTO(
            first_name=data["first_name"],
            last_name=data["last_name"],
            role=Role(data["role"]),
            group_name=data["group_name"],
            telegram_id=int(data["telegram_id"]),
            university_alias=UniversityAlias(data["university_alias"]),
            birthdate=None if data["birthdate"] == "0" else date.fromisoformat(data["birthdate"]),
        )
