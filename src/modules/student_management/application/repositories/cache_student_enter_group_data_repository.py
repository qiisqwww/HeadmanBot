from abc import ABC, abstractmethod

from .student_enter_group_dto import StudentEnterGroupDTO

__all__ = [
    "CacheStudentEnterGroupDataRepository",
]


class CacheStudentEnterGroupDataRepository(ABC):
    @abstractmethod
    async def cache(self, data: StudentEnterGroupDTO) -> None:
        ...

    @abstractmethod
    async def fetch(self, telegram_id: int) -> StudentEnterGroupDTO | None:
        ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None:
        ...
