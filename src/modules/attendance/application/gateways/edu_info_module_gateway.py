from abc import ABC, abstractmethod

from src.modules.attendance.domain import GroupInfo

__all__ = [
    "EduInfoModuleGateway",
]


class EduInfoModuleGateway(ABC):
    @abstractmethod 
    async def fetch_all_groups(self) -> list[GroupInfo]:
        ...
