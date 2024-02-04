from abc import abstractmethod, ABC

from src.modules.common.domain import UniversityAlias
from src.modules.edu_info.contract import EduInfoModuleContract
from src.modules.student_management.domain import EduProfileInfo, Group, UniversityInfo

__all__ = [
    "EduInfoModuleGateway",
]


class EduInfoModuleGateway(ABC):
    _contract: EduInfoModuleContract

    @abstractmethod
    def __init__(self, contract: EduInfoModuleContract) -> None:
        ...

    @abstractmethod
    async def get_all_universities_info(self) -> list[UniversityInfo]:
        ...

    @abstractmethod
    async def get_university_info_by_alias(self, alias: UniversityAlias) -> UniversityInfo:
        ...

    @abstractmethod
    async def find_group_by_id(self, group_id: int) -> Group | None:
        ...

    @abstractmethod
    async def find_group_by_name(self, group_name: str) -> Group | None:
        ...

    @abstractmethod
    async def find_group_by_name_and_alias(self, group_name: str, university_alias: UniversityAlias) -> Group | None:
        ...

    @abstractmethod
    async def create_group(self, group_name: str, university_id: int) -> Group:
        ...

    @abstractmethod
    async def get_edu_profile_info(self, group_id: int) -> EduProfileInfo | None:
        ...
