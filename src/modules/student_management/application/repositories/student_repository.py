from abc import ABC, abstractmethod

from src.modules.student_management.domain import Role, Student

from .create_student_dto import CreateStudentDTO

__all__ = [
    "StudentRepository",
]


class StudentRepository(ABC):
    @abstractmethod
    async def find_by_id(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def find_by_group_name_and_role(self, group_name: str, role: Role) -> Student | None:
        ...

    @abstractmethod
    async def create(
        self,
        student_data: CreateStudentDTO,
        group_id: int,
    ) -> Student:
        ...

    # @abstractmethod
    # async def all(self) -> list[Student]:
    #     ...
    #
    # @abstractmethod
    # async def filter_group_by_id(self, group_id: GroupId) -> list[Student] | None:
    #     ...

    #
    # @abstractmethod
    # async def update_surname_by_id(self, new_surname: str, student_id: StudentId) -> None:
    #     ...
    #
    # @abstractmethod
    # async def update_name_by_id(self, new_name: str, student_id: StudentId) -> None:
    #     ...
