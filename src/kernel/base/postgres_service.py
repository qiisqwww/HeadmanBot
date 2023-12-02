from asyncpg.pool import PoolConnectionProxy

__all__ = [
    "PostgresService",
]


class PostgresService:
    _con: PoolConnectionProxy

    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
