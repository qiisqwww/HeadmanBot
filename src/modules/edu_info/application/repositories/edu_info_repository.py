from abc import ABC, abstractmethod

__all__ = [
    "EduInfoRepository",
]


class EduInfoRepository(ABC):
    @abstractmethod
    async def get_group_and_uni_name_by_group_id(self, group_id: int) -> tuple[str, str] | None:
        ...
