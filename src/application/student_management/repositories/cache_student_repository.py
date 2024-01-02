from abc import ABC, abstractmethod

from .create_student_dto import CreateStudentDTO

__all__ = [
    "CacheStudentDataRepository",
]


class CacheStudentDataRepository(ABC):
    @abstractmethod
    async def cache(self, data: CreateStudentDTO) -> None:
        ...

    @abstractmethod
    async def pop(self, student_id: int) -> CreateStudentDTO:
        ...
