from abc import abstractmethod

from src.dto import GroupId, Student, StudentRaw

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "StudentRepository",
]


class StudentRepository(PostgresRepository):
    @abstractmethod
    async def create_and_return(
        self,
        student_raw: StudentRaw,
        group_id: GroupId,
    ) -> Student:
        ...

    @abstractmethod
    async def find(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def all(self) -> list[Student]:
        ...
