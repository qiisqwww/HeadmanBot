from typing import Protocol

from asyncpg.pool import PoolConnectionProxy

from src.kernel.abstracts import AbstractStudent

__all__ = [
    "PermissionsServiceProtocol",
]


class PermissionsServiceProtocol(Protocol):
    def __init__(self, con: PoolConnectionProxy) -> None:
        ...

    async def check_is_student_registered_and_return(self, telegram_id: int) -> AbstractStudent | None:
        ...

    async def check_is_headman(self, student: AbstractStudent) -> bool:
        ...
