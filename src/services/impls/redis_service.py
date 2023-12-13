from redis.asyncio import Redis  # type: ignore

from src.services.interfaces import Service

__all__ = [
    "RedisService",
]


class   RedisService(Service):
    _con: Redis

    def __init__(self, con: Redis) -> None:
        self._con = con
