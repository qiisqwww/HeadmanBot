from abc import abstractmethod

from src.modules.common.application import Dependency

__all__ = [
    "EduInfoRepository",
]


class EduInfoRepository(Dependency):
    @abstractmethod
    async def get_group_and_uni_name_by_group_id(self, group_id: int) -> tuple[str, str] | None:
        ...
