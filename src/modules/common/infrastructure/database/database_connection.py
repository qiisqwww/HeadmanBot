import sys
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any, ClassVar, Final, Self

from asyncpg import Record, create_pool
from asyncpg.pool import Pool, PoolConnectionProxy
from asyncpg.transaction import Transaction
from loguru import logger

from src.modules.common.infrastructure.config.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    DEBUG,
)

__all__ = [
    "DbContext",
]

if TYPE_CHECKING:
    type DatabaseConnection = PoolConnectionProxy[Record]
    type DatabaseConnectionPool = Pool[Record]
else:
    type DatabaseConnection = PoolConnectionProxy
    type DatabaseConnectionPool = Pool


class DbContext:
    _db_pool: ClassVar[DatabaseConnectionPool]
    _DATABASE_URL: Final[str] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    _con: DatabaseConnection

    def __init__(self) -> None:
        """Don't use default constructor. Please, use instead new classmethod."""
        msg = "Use classmethod new instead of __init__"
        raise RuntimeWarning(msg)

    @classmethod
    async def init(cls: type[Self]) -> None:
        await cls._create_pool()

    @classmethod
    async def new(cls: type[Self]) -> Self:
        """Create new DbContext instead of __init__ method."""
        new_connection = cls.__new__(cls)
        new_connection._con = await cls._db_pool.acquire()  # noqa: SLF001 , PGH003# pyright: ignore
        return new_connection

    async def close(self) -> None:
        await self._db_pool.release(self._con)

    @classmethod
    async def close_pool(cls: type[Self]) -> None:
        """Close pool for finalization resources."""
        await cls._db_pool.close()

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
        *args: object,
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

    @classmethod
    async def _create_pool(cls: type[Self]) -> None:
        gotten_pool = await create_pool(cls._DATABASE_URL, record_class=Record)

        if gotten_pool is None:
            logger.error("Cannot connect to postgres.")
            sys.exit(-1)

        cls._db_pool = gotten_pool
