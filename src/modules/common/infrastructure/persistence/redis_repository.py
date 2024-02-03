from typing import TYPE_CHECKING, TypeAlias

from injector import inject
from redis.asyncio import Redis

__all__ = [
    "RedisRepositoryImpl",
]

if TYPE_CHECKING:
    RedisConnection: TypeAlias = Redis[str]
else:
    RedisConnection: TypeAlias = Redis

class RedisRepositoryImpl:
    _con: RedisConnection

    @inject
    def __init__(self, con: RedisConnection) -> None:
        self._con = con
