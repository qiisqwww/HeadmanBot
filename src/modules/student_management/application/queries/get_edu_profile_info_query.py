from injector import inject

from src.modules.common.application import Dependency
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import EduProfileInfo

__all__ = [
    "GetEduProfileInfoQuery",
]


class GetEduProfileInfoQuery(Dependency):
    _gateway: EduInfoModuleGateway

    @inject
    def __init__(self, gateway: EduInfoModuleGateway) -> None:
        self._gateway = gateway

    async def execute(self, group_id: int) -> EduProfileInfo | None:
        return await self._gateway.get_edu_profile_info(group_id)
