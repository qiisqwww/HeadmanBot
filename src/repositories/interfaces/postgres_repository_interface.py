from abc import ABC, abstractmethod

from asyncpg.pool import PoolConnectionProxy

__all__ = [
    "PostgresRepository",
]


class PostgresRepository(ABC):
    @abstractmethod
    def __init__(self, con: PoolConnectionProxy) -> None:
        ...
