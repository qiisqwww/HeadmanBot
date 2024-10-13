from collections.abc import Iterable, Sequence
from typing import Any, Self

import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool, PoolConnectionProxy
from asyncpg.transaction import Transaction
from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from src.common.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_HOST,
    REDIS_PORT,
)

__all__ = [
    "Context",
]


class Context:
    _con: PoolConnectionProxy
    _redis_con: Redis

    _pool: Pool | None
    _redis_pool: ConnectionPool | None

    def __init__(self, pool: Pool | None = None, redis_pool: ConnectionPool | None = None) -> None:
        self._pool = pool
        self._redis_pool = redis_pool

    async def __aenter__(self) -> Self:
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def open(self) -> None:
        if self._pool is None:
            self._con = await asyncpg.connect(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            self._redis_con = Redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True")
        else:
            self._con = await self._pool.acquire()
            self._redis_con = Redis(connection_pool=self._redis_pool)

    async def close(self) -> None:
        if self._pool is None:
            await self._con.close()
        else:
            await self._pool.release(self._con)

    async def transaction(self) -> Transaction:
        return self._con.transaction()

    async def fetch(
            self,
            query: str,
            *args: object,
            timeout: float | None = None,
    ) -> list[Record]:
        self._log_query(query, args)
        return await self._con.fetch(query, *args, timeout=timeout)

    async def fetchrow(
            self,
            query: str,
            *args: object,
            timeout: float | None = None,
    ) -> Record | None:
        self._log_query(query, args)
        return await self._con.fetchrow(query, *args, timeout=timeout)

    async def fetchval(
            self,
            query: str,
            *args: object,
            timeout: float | None = None,
    ) -> Any:  # noqa: ANN401
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
        self._log_query(query, args)
        return await self._con.execute(query, *args, timeout=timeout)

    @staticmethod
    def _log_query(query: str, args: Iterable[Any]) -> None:
        for i, arg in enumerate(args, start=1):
            query = query.replace(f"${i}", str(arg))

        query = " ".join(query.split())

        logger.log("SQL", query)
