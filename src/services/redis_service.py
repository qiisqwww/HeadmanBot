from loguru import logger

import redis.asyncio as redis

from src.config import REDIS_PORT, REDIS_HOST


__all__ = ["RedisService"]


class RedisService:
    _con: redis.Redis

    async def set_user_throttling(self, user_id: str) -> None:
        await self._con.set("thr"+user_id, 0, ex=60)

    async def increase_user_throttling(self, user_id: str) -> None:
        await self._con.incr("thr"+user_id)

    async def get_user_throttling(self, user_id: str) -> int:
        return await self._con.get("thr"+user_id)

    async def __aenter__(self) -> "RedisService":
        self._con = redis.Redis(host=REDIS_HOST,
                                port=REDIS_PORT,
                                decode_responses=True)
        return self

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        await self._con.aclose()
