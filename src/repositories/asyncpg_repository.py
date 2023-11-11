from typing import TypeVar

from asyncpg.pool import PoolConnectionProxy

from .async_repository import AsyncRepository

__all__ = [
    "AsyncpgRepository",
]

DTO = TypeVar("DTO")


class AsyncpgRepository(AsyncRepository[DTO]):
    _con: PoolConnectionProxy

    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
