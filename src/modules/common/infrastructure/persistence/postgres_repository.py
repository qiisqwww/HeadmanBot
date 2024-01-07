from asyncpg.pool import PoolConnectionProxy

__all__ = [
    "PostgresRepositoryImpl",
]


class PostgresRepositoryImpl:
    _con: PoolConnectionProxy

    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
