from typing import Self

from loguru import logger
from redis.asyncio import Redis

from src.config import REDIS_HOST, REDIS_PORT

__all__ = [
    "RedisService",
]


class RedisService:
    _con: Redis

    async def __aenter__(self) -> Self:
        self._con = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        return self

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        await self._con.close()
