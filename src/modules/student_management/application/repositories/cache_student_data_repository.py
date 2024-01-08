from abc import abstractmethod

from src.modules.common.application.dependency import Dependency

from .create_student_dto import CreateStudentDTO

__all__ = [
    "CacheStudentDataRepository",
]


class CacheStudentDataRepository(Dependency):
    @abstractmethod
    async def cache(self, data: CreateStudentDTO) -> None:
        ...

    @abstractmethod
    async def pop(self, telegram_id: int) -> CreateStudentDTO | None:
        ...
