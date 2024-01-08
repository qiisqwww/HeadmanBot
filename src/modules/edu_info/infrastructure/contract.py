from dataclasses import asdict
from typing import Any, final

from injector import inject

from src.modules.common.domain import UniversityAlias
from src.modules.edu_info.application.repositories import (
    GroupRepository,
    UniversityRepository,
)
from src.modules.edu_info.contract import EduInfoModuleContract

__all__ = [
    "EduInfoModuleContractImpl",
]


@final
class EduInfoModuleContractImpl(EduInfoModuleContract):
    _university_repository: UniversityRepository
    _group_repository: GroupRepository

    @inject
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

    async def get_group_info_by_group_name(self, group_name: str) -> dict[str, Any] | None:
        group = await self._group_repository.find_by_name(group_name)

        if group is None:
            return None

        return asdict(group)

    async def get_group_info_by_group_name_and_alias(
        self, group_name: str, alias: UniversityAlias
    ) -> dict[str, Any] | None:
        group = await self._group_repository.find_by_name_and_uni(group_name, alias)

        if group is None:
            return None

        return asdict(group)

    async def create_group(self, group_name: str, university_id: int) -> dict[str, Any]:
        group = await self._group_repository.create(group_name, university_id)
        return asdict(group)

    async def get_university_info_by_alias(self, alias: UniversityAlias) -> dict[str, Any]:
        university = await self._university_repository.get_by_alias(alias)
        return asdict(university)