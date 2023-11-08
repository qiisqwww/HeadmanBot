from loguru import logger

import redis

from src.config import REDIS_PORT, REDIS_HOST


__all__ = ["RedisService"]


class RedisService:
    _con: redis.Redis

    def __init__(self) -> None:
        self._con = redis.Redis(host=REDIS_HOST,
                                port=REDIS_PORT,
                                decode_responses=True)

    def set_user_throttling(self, user_id: str) -> None:
        self._con.set("thr"+user_id, 0, ex=10)

    def increase_user_throttling(self, user_id: str) -> None:
        self._con.incr("thr"+user_id)

    def get_user_throttling(self, user_id: str) -> int:
        return self._con.get("thr"+user_id)

    def __enter__(self) -> "RedisService":
        return self

    def __exit__(self, exc_type, *_) -> None:
        if exc_type is not None:
            logger.error(exc_type)

        self._con.close()
