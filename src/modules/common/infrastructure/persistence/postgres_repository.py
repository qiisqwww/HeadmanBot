from asyncpg.pool import PoolConnectionProxy
from injector import inject

__all__ = [
    "PostgresRepositoryImpl",
]


class PostgresRepositoryImpl:
    _con: PoolConnectionProxy

    @inject
    def __init__(self, con: PoolConnectionProxy) -> None:
        self._con = con
