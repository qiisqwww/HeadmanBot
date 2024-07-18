from abc import ABC, abstractmethod

from .create_student_dto import CreateStudentDTO

__all__ = [
    "CacheCreateStudentDataRepository",
]


class CacheCreateStudentDataRepository(ABC):
    @abstractmethod
    async def cache(self, data: CreateStudentDTO) -> None:
        ...

    @abstractmethod
    async def fetch(self, telegram_id: int) -> CreateStudentDTO | None:
        ...

    @abstractmethod
    async def delete(self, telegram_id: int) -> None:
        ...
