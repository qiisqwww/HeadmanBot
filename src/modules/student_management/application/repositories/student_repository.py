from abc import abstractmethod

from src.modules.common.application.dependency import Dependency
from src.modules.student_management.domain import Role, Student

from .create_student_dto import CreateStudentDTO

__all__ = [
    "StudentRepository",
]


class StudentRepository(Dependency):
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
