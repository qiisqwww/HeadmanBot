from dataclasses import asdict
from typing import Any

from src.modules.edu_info.application.repositories import (
    GroupRepository,
    UniversityRepository,
)
from src.modules.edu_info.contract import EduInfoModuleContract

__all__ = [
    "EduInfoModuleContractImpl",
]


class EduInfoModuleContractImpl(EduInfoModuleContract):
    _university_repository: UniversityRepository
    _group_repository: GroupRepository

    def __init__(self, university_repository: UniversityRepository, group_repository: GroupRepository) -> None:
        self._university_repository = university_repository
        self._group_repository = group_repository

    async def get_all_universities_info(self) -> list[dict[str, Any]]:
        universities = await self._university_repository.all()
        return [asdict(uni) for uni in universities]

    async def get_group_info_by_group_id(self, group_id: int) -> dict[str, Any] | None:
        group = await self._group_repository.find_by_id(group_id)

        if group is None:
            return None

        return asdict(group)
