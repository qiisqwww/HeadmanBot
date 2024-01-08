from injector import inject
from redis.asyncio import Redis

__all__ = [
    "RedisRepositoryImpl",
]


class RedisRepositoryImpl:
    _con: Redis

    @inject
    def __init__(self, con: Redis) -> None:
        self._con = con
