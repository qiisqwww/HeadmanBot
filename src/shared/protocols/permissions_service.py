from typing import Protocol

from asyncpg.pool import PoolConnectionProxy

from .abstract_student import AbstractStudent

__all__ = [
    "PermissionsService",
]


class PermissionsService(Protocol):
    def __init__(self, con: PoolConnectionProxy) -> None:
        ...

    async def find_student(self, telegram_id: int) -> AbstractStudent | None:
        ...

    async def is_headman(self, student: AbstractStudent) -> bool:
        ...
