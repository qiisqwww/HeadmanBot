from abc import abstractmethod

from src.dto.models import GroupId, Student, StudentLoginData, StudentId
from src.repositories import StudentRepository

from .group_service_interface import GroupService
from .service import Service

__all__ = [
    "StudentService",
]


class StudentService(Service):
    @abstractmethod
    def __init__(self, student_repository: StudentRepository, group_service: GroupService) -> None:
        ...

    @abstractmethod
    async def find(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def all(self) -> list[Student]:
        ...

    @abstractmethod
    async def filter_by_group_id(self, group_id: GroupId) -> list[Student] | None:
        ...

    @abstractmethod
    async def register_student(self, student: StudentLoginData) -> None:
        ...

    @abstractmethod
    async def get_headman_by_group_name(self, group_name: str) -> Student | None:
        ...

    @abstractmethod
    async def update_surname_by_id(self, new_surname: str, student_id: StudentId) -> None:
        ...

    @abstractmethod
    async def update_name_by_id(self, new_name: str, student_id: StudentId) -> None:
        ...