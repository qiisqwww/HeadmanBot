from collections.abc import Callable
from typing import TYPE_CHECKING, ClassVar, Final, NoReturn, Self

from aiogram import Bot
from injector import Binder, Injector, InstanceProvider, Provider, singleton
from redis.asyncio import Connection, ConnectionPool, Redis

from src.modules.attendance.infrastructure.container import assemble_attendance_module
from src.modules.common.application import UnitOfWork
from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.common.infrastructure.bot_notifier import BotNotifierImpl
from src.modules.common.infrastructure.config.config import (
    REDIS_HOST,
    REDIS_PORT,
)
from src.modules.common.infrastructure.database.database_connection import DbContext
from src.modules.common.infrastructure.uow import UnitOfWorkImpl
from src.modules.edu_info.infrastructure.container import assemble_edu_info_module
from src.modules.student_management.infrastructure.container import (
    assemble_student_management_module,
)
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.infrastructure import ScheduleApiImpl
from src.modules.utils.throttling.application.repositories import ThrottlingRepository
from src.modules.utils.throttling.infrastructure import ThrottlingRepositoryImpl

__all__ = [
    "Container",
]


def singleton_bind[T](binder: Binder, interface: type[T], to: T | Provider[T] | Callable[..., T]) -> None:
    binder.bind(interface, to, singleton)


if TYPE_CHECKING:
    type RedisConnection = Redis[str]
    type RedisPool = ConnectionPool[Connection]
else:
    type RedisConnection = Redis
    type RedisPool = ConnectionPool


class Container:
    _redis_pool: ClassVar[RedisPool]
    _bot: ClassVar[Bot]

    _REDIS_URL: Final[str] = f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"

    _injector: Injector
    _db_ctx: DbContext
    _redis_con: RedisConnection

    @classmethod
    async def close(cls: type[Self]) -> None:
        await DbContext.close_pool()
        await cls._redis_pool.disconnect()

    @classmethod
    async def init(cls: type[Self], bot: Bot) -> None:
        cls._bot = bot

        await DbContext.init()
        cls._redis_pool = ConnectionPool.from_url(cls._REDIS_URL)  # type: ignore  # noqa: PGH003

    async def __aenter__(self) -> Self:
        await self._build_dependencies()
        return self

    async def __aexit__(self, *_: object) -> None:
        await self._db_ctx.close()
        await self._redis_con.aclose()  # type: ignore  # noqa: PGH003

    def has_dependency(self, interface: type) -> bool:
        try:
            self._injector.get(interface)
        except:
            return False
        else:
            return True

    def get_dependency[T](self, interface: type[T]) -> T | NoReturn:
        return self._injector.get(interface)

    async def _build_dependencies(self) -> None:
        self._redis_con = Redis(connection_pool=Container._redis_pool)
        self._db_ctx = await DbContext.new()

        def _assemble_modules(binder: Binder) -> None:
            singleton_bind(
                binder,
                type[ScheduleAPI],
                to=InstanceProvider(ScheduleApiImpl),
            )
            singleton_bind(binder, UnitOfWork, to=UnitOfWorkImpl)
            singleton_bind(binder, ThrottlingRepository, ThrottlingRepositoryImpl)
            singleton_bind(binder, Bot, self._bot)

            assemble_edu_info_module(binder)
            assemble_student_management_module(binder)
            assemble_attendance_module(binder)

        self._injector = Injector(_assemble_modules)

        singleton_bind(self._injector.binder, DbContext, to=self._db_ctx)
        singleton_bind(self._injector.binder, Redis, to=self._redis_con)
        singleton_bind(self._injector.binder, BotNotifier, BotNotifierImpl)
