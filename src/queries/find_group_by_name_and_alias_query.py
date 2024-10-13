from typing import final

from injector import inject

from src.common import UniversityAlias
from src.common import UseCase
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import Group

__all__ = [
    "FindGroupByNameAndAliasQuery",
]


@final
class FindGroupByNameAndAliasQuery(UseCase):
    _edu_info_module_gateway: EduInfoModuleGateway

    @inject
    def __init__(self, gateway: EduInfoModuleGateway) -> None:
        self._edu_info_module_gateway = gateway

    async def execute(self, group_name: str, university_alias: UniversityAlias) -> Group | None:
        return await self._edu_info_module_gateway.find_group_by_name_and_alias(group_name, university_alias)
