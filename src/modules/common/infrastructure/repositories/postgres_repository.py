from typing import TYPE_CHECKING, TypeAlias

from asyncpg.pool import PoolConnectionProxy
from injector import inject

__all__ = [
    "PostgresRepositoryImpl",
]

if TYPE_CHECKING:
    from asyncpg import Record
    DatabaseConnection: TypeAlias = PoolConnectionProxy[Record]
else:
    DatabaseConnection: TypeAlias = PoolConnectionProxy

class PostgresRepositoryImpl:
    _con: DatabaseConnection

    @inject
    def __init__(self, con: DatabaseConnection) -> None:
        self._con = con
