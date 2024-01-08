from typing import final

from injector import inject

from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import Group, UniversityInfo

__all__ = [
    "EduInfoModuleGatewayImpl",
]


@final
class EduInfoModuleGatewayImpl(EduInfoModuleGateway):
    _contract: EduInfoModuleContract

    @inject
    def __init__(self, contract: EduInfoModuleContract) -> None:
        self._contract = contract

    async def get_all_universities_info(self) -> list[UniversityInfo]:
        universities_info = await self._contract.get_all_universities_info()

        return [UniversityInfo(**university_info) for university_info in universities_info]

    async def get_university_info_by_alias(self, alias: UniversityAlias) -> UniversityInfo:
        university_info = await self._contract.get_university_info_by_alias(alias)
        return UniversityInfo(**university_info)

    async def find_group_by_id(self, group_id: int) -> Group | None:
        group_info = await self._contract.get_group_info_by_group_id(group_id)

        if group_info is None:
            return None

        return Group(**group_info)

    async def find_group_by_name(self, group_name: str) -> Group | None:
        group_info = await self._contract.get_group_info_by_group_name(group_name)

        if group_info is None:
            return None

        return Group(**group_info)

    async def find_group_by_name_and_alias(self, group_name: str, university_alias: UniversityAlias) -> Group | None:
        group_info = await self._contract.get_group_info_by_group_name_and_alias(group_name, university_alias)

        if group_info is None:
            return None

        return Group(**group_info)

    async def create_group(self, group_name: str, university_id: int) -> Group:
        group_info = await self._contract.create_group(group_name, university_id)
        return Group(**group_info)
