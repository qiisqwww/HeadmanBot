import logging

from asyncpg import Connection

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
            logging.error(exc_type)

        logging.info("disconnected from database")

        await self._con.close()
