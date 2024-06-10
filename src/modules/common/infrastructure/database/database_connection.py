from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any

from loguru import logger
from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from asyncpg.transaction import Transaction
from ..config import DEBUG

__all__ = [
    "DatabaseConnection",
]

if TYPE_CHECKING:
    type Connection = PoolConnectionProxy[Record]
else:
    type Connection = PoolConnectionProxy


class DatabaseConnection:
    _con: Connection

    def __init__(self, con: Connection) -> None:
        self._con = con

    @property
    def connection(self) -> Connection:
        return self._con

    async def transaction(self) -> Transaction:
        return self._con.transaction()

    async def fetch(
        self,
        query: str,
        *args: object,
        timeout: float | None = None,
    ) -> list[Record]:
        if DEBUG:
            self._log_query(query, args)
        return await self._con.fetch(query, *args, timeout=timeout)

    async def fetchrow(
        self,
        query: str,
        *args: object,
        timeout: float | None = None,
    ) -> Record | None:
        if DEBUG:
            self._log_query(query, args)
        return await self._con.fetchrow(query, *args, timeout=timeout)

    async def fetchval(
        self,
        query: str,
        *args: object,
        timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
        if DEBUG:
            self._log_query(query, args)
        return await self._con.fetchval(query, *args, timeout=timeout)

    async def executemany(
        self,
        command: str,
        args: Iterable[Sequence[Any]],
        timeout: float | None = None,
    ) -> None:
        return await self._con.executemany(command, args, timeout=timeout)

    async def execute(
        self,
        query: str,
        *args: Any,
        timeout: float | None = None,
    ) -> str:
        if DEBUG:
            self._log_query(query, args)
        return await self._con.execute(query, *args, timeout=timeout)

    @staticmethod
    def _log_query(query: str, args: Iterable[Any]) -> None:
        for i, arg in enumerate(args, start=1):
            query = query.replace(f"${i}", str(arg))

        query = " ".join(query.split())

        logger.debug(f"SQL query: {query}")
