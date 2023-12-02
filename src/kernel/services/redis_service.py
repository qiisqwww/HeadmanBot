from redis.asyncio import Redis  # type: ignore

__all__ = [
    "RedisService",
]


class RedisService:
    _con: Redis

    def __init__(self, con: Redis) -> None:
        self._con = con