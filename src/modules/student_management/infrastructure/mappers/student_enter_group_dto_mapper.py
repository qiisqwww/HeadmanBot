from collections.abc import Mapping
from typing import final

from src.modules.common.domain import UniversityAlias
from src.modules.student_management.application.repositories import StudentEnterGroupDTO
from src.modules.student_management.domain import Role

__all__ = [
    "StudentEnterGroupDTOMapper",
]


@final
class StudentEnterGroupDTOMapper:
    def to_redis_dict(self, data: StudentEnterGroupDTO) -> Mapping[bytes | str, str]:
        return {
            "role":  data.role.value,
            "group_name": data.group_name,
            "telegram_id":  str(data.telegram_id),
            "university_alias": data.university_alias.value,
        }

    def from_redis_dict(self, data: Mapping[str, str]) -> StudentEnterGroupDTO:
        return StudentEnterGroupDTO(
            role=Role(data["role"]),
            group_name=data["group_name"],
            telegram_id=int(data["telegram_id"]),
            university_alias=UniversityAlias(data["university_alias"])
        )