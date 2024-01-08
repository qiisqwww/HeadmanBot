from typing import final

from injector import inject

from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.student_management.application.gateways import EduInfoModuleGateway
from src.modules.student_management.domain import UniversityInfo

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
