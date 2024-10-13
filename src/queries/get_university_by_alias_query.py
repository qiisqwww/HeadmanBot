from injector import inject

from src.common import UniversityAlias
from src.common import UseCase
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import UniversityInfo

__all__ = [
    "GetUniversityByAliasQuery",
]


class GetUniversityByAliasQuery(UseCase):
    _edu_info_module_gateway: EduInfoModuleGateway

    @inject
    def __init__(self, gateway: EduInfoModuleGateway) -> None:
        self._edu_info_module_gateway = gateway

    async def execute(self, alias: UniversityAlias) -> UniversityInfo:
        return await self._edu_info_module_gateway.get_university_info_by_alias(alias)
