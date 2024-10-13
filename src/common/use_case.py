from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

from redis.asyncio import Redis

from src.common.database import DbContext

__all__ = [
    "UseCase",
    "NoArgsUseCase",
    "WithArgsUseCase",
]

if TYPE_CHECKING:
    RedisConnection = Redis[str]
else:
    RedisConnection = Redis


class UseCase(ABC):  # noqa: B024
    @abstractmethod
    def __init__(self, con: DbContext | None = None, redis_con: RedisConnection | None = None) -> None:
        ...


class NoArgsUseCase(UseCase):
    @abstractmethod
    def execute(self) -> Any:  # noqa: ANN401
        ...


class WithArgsUseCase(UseCase):
    @abstractmethod
    def execute(self, *args: object) -> Any:  # noqa: ANN401
        ...
