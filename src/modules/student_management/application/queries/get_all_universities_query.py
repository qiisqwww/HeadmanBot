from injector import inject

from src.modules.common.application import Dependency
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import UniversityInfo

__all__ = [
    "GetAllUniversitiesQuery",
]


class GetAllUniversitiesQuery(Dependency):
    _gateway: EduInfoModuleGateway

    @inject
    def __init__(self, gateway: EduInfoModuleGateway) -> None:
        self._gateway = gateway

    async def execute(self) -> list[UniversityInfo]:
        return await self._gateway.get_all_universities_info()
