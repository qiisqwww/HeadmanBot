from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.student_management.domain import UniversityInfo

__all__ = [
    "EduInfoModuleGatewayImpl",
]


class EduInfoModuleGatewayImpl:
    _contract: EduInfoModuleContract

    def __init__(self, contract: EduInfoModuleContract) -> None:
        self._contract = contract

    async def get_all_universities_info(self) -> list[UniversityInfo]:
        universities_info = await self._contract.get_all_universities_info()

        return [UniversityInfo(**university_info) for university_info in universities_info]
