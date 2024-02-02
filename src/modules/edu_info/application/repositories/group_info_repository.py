from abc import ABC, abstractmethod

from src.modules.edu_info.domain import GroupInfo

__all__ = [
    "GroupInfoRepository",
]

class GroupInfoRepository(ABC):
    @abstractmethod 
    async def fetch_all(self) -> list[GroupInfo]:
        ...
