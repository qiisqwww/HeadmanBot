from asyncpg import Connection
from loguru import logger

from ..database.db import get_db_connection

__all__ = [
    "Service",
]


class Service:
    _con: Connection

    async def __aenter__(self):
        self._con = await get_db_connection()
        return self

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        logger.trace("disconnected from database")

        await self._con.close()
