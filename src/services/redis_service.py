from loguru import logger
from typing import Self

import redis.asyncio as redis

from src.config import REDIS_PORT, REDIS_HOST
from src.enums.university_id import UniversityId


__all__ = ["RedisService"]


class RedisService:
    _con: redis.Redis

    async def set_user_throttling(self, user_id: str) -> None:
        await self._con.set(f"thr{user_id}", 0, ex=60)

    async def increase_user_throttling(self, user_id: str) -> None:
        await self._con.incr(f"thr{user_id}")

    async def get_user_throttling(self, user_id: str) -> int:
        return await self._con.get(f"thr{user_id}")

    async def insert_preregistration_user(self, user_data: dict):
        await self._con.hmset(user_data["telegram_id"], user_data)
        await self._con.expire(user_data["telegram_id"], 86400)

    async def get_and_remove_user(self, user_id: str) -> dict:
        query = await self._con.hgetall(user_id)
        query["university_id"] = UniversityId.MIREA

        await self._con.hdel(user_id, *query.keys())
        return query

    async def __aenter__(self) -> Self:
        self._con = redis.Redis(host=REDIS_HOST,
                                port=REDIS_PORT,
                                decode_responses=True)
        return self

    async def __aexit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        await self._con.aclose()
