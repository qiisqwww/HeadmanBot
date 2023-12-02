from typing import Protocol

from asyncpg.pool import PoolConnectionProxy

from src.kernel.student_dto import StudentDTO

__all__ = [
    "FindStudentServiceProtocol",
]


class FindStudentServiceProtocol(Protocol):
    def __init__(self, con: PoolConnectionProxy) -> None:
        ...

    async def find_student(self, telegram_id: int) -> StudentDTO | None:
        ...
