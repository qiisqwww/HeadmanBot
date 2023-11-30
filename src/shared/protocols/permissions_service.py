from typing import Protocol

from asyncpg.pool import PoolConnectionProxy

from src.dto import Student


class PermissionsService(Protocol):
    def __init__(self, con: PoolConnectionProxy) -> None:
        ...

    async def find_student(self, telegram_id: int) -> Student | None:
        ...

    async def is_headman(self, student: Student) -> bool:
        ...
