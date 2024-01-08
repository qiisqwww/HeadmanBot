from injector import inject

from src.modules.common.application import Dependency
from src.modules.common.domain import UniversityAlias
from src.modules.student_management.application.gateways import EduInfoModuleGateway

__all__ = [
    "IsGroupRegisteredQuery",
]


class IsGroupRegisteredQuery(Dependency):
    _edu_info_module_gateway: EduInfoModuleGateway

    @inject
    def __init__(self, gateway: EduInfoModuleGateway) -> None:
        self._edu_info_module_gateway = gateway

    async def execute(self, group_name: str, university_alias: UniversityAlias) -> bool:
        return (
            await self._edu_info_module_gateway.find_group_by_name_and_alias(group_name, university_alias)
        ) is not None
