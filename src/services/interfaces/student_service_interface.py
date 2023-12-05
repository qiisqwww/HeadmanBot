from abc import abstractmethod

from src.dto import Student
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
