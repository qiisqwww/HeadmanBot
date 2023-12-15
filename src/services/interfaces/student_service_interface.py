from abc import abstractmethod

from src.dto import Student, StudentRaw
from src.dto.group import GroupId
from src.repositories import StudentRepository

from .service import Service

__all__ = [
    "StudentService",
]


class StudentService(Service):
    @abstractmethod
    def __init__(
        self,
        student_repository: StudentRepository,
    ) -> None:
        ...

    @abstractmethod
    async def find(self, telegram_id: int) -> Student | None:
        ...

    @abstractmethod
    async def all(self) -> list[Student]:
        ...

    @abstractmethod
    async def group_has_headman(self, group_id: GroupId) -> bool:
        ...

    @abstractmethod
    async def filter_by_group_id(self, group_id: GroupId) -> list[Student] | None:
        ...

    @abstractmethod
    async def register_student(self, student: StudentRaw) -> None:
        ...
