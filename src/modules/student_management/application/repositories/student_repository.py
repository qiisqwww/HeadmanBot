from abc import ABC, abstractmethod
from datetime import date

from src.modules.student_management.domain import Role, Student

from .create_student_dto import CreateStudentDTO

__all__ = [
    "StudentRepository",
]


class StudentRepository(ABC):
    @abstractmethod
    async def find_by_id(self, student_id: int) -> Student | None:
        ...

    @abstractmethod
    async def find_by_telegram_id(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def find_by_group_id_and_role(self, group_id: int, role: Role) -> Student | None:
        ...

    @abstractmethod
    async def create(
        self,
        student_data: CreateStudentDTO,
        group_id: int,
    ) -> Student:
        ...

    @abstractmethod
    async def update_is_checked_in(self, student_id: int, new_is_checked_in: bool) -> None:
        ...

    @abstractmethod
    async def update_is_checked_in_all(self, new_is_checked_in: bool) -> None:
        ...

    @abstractmethod
    async def update_first_name_by_id(self, student_id: int, new_first_name: str) -> None:
        ...

    @abstractmethod
    async def update_last_name_by_id(self, student_id: int, new_last_name: str) -> None:
        ...

    @abstractmethod
    async def update_birthdate_by_id(self, student_id: int, new_date: date | None) -> None:
        ...
