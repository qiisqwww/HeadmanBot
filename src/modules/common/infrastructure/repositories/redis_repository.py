from typing import TYPE_CHECKING

from injector import inject
from redis.asyncio import Redis

__all__ = [
    "RedisRepositoryImpl",
]

if TYPE_CHECKING:
    RedisConnection = Redis[str]
else:
    RedisConnection = Redis


class RedisRepositoryImpl:
    _con: RedisConnection

    @inject
    def __init__(self, con: RedisConnection) -> None:
        self._con = con
