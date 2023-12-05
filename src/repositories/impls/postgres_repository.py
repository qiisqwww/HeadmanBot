from asyncpg.pool import PoolConnectionProxy

from ..interfaces import PostgresRepository

__all__ = [
    "PostgresRepositoryImpl",
]


class PostgresRepositoryImpl(PostgresRepository):
    _con: PoolConnectionProxy

    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
