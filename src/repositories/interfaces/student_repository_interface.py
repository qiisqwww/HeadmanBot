from abc import abstractmethod

from src.dto.models import GroupId, Student, StudentLoginData, StudentId
from src.enums import Role

from .postgres_repository_interface import PostgresRepository

__all__ = [
    "StudentRepository",
]


class StudentRepository(PostgresRepository):
    @abstractmethod
    async def create_and_return(
        self,
        student_raw: StudentLoginData,
        group_id: GroupId,
    ) -> Student:
        ...

    @abstractmethod
    async def find_by_id(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def all(self) -> list[Student]:
        ...

    @abstractmethod
    async def filter_group_by_id(self, group_id: GroupId) -> list[Student] | None:
        ...

    @abstractmethod
    async def find_by_group_id_and_role(self, group_id: GroupId, role: Role) -> Student | None:
        ...

    @abstractmethod
    async def update_surname_by_id(self, new_surname: str, student_id: StudentId) -> None:
        ...

    @abstractmethod
    async def update_name_by_id(self, new_name: str, student_id: StudentId) -> None:
        ...
