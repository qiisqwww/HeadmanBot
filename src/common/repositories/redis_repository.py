from typing import TYPE_CHECKING

from redis.asyncio import Redis

__all__ = [
    "RedisRepository",
]

if TYPE_CHECKING:
    RedisConnection = Redis[str]
else:
    RedisConnection = Redis


class RedisRepository:
    _con: RedisConnection

    def __init__(self, con: RedisConnection) -> None:
        self._con = con
