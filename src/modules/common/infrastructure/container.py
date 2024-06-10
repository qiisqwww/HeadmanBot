from collections.abc import Callable
from sys import exit
from typing import TYPE_CHECKING, ClassVar, Final, NoReturn, Self

from aiogram import Bot
from asyncpg import Pool, Record, create_pool
from injector import Binder, Injector, InstanceProvider, Provider, singleton
from loguru import logger
from redis.asyncio import ConnectionPool, Redis

from src.modules.attendance.infrastructure.container import assemble_attendance_module
from src.modules.common.application import UnitOfWork
from src.modules.common.application.bot_notifier import BotNotifier
from src.modules.common.infrastructure.bot_notifier import BotNotifierImpl
from src.modules.common.infrastructure.config.config import (
    DB_HOST,
    DB_NAME,
    DB_PASS,
    DB_PORT,
    DB_USER,
    REDIS_HOST,
    REDIS_PORT,
)
from src.modules.common.infrastructure.uow import DatabaseConnection, UnitOfWorkImpl
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
    type DatabaseConnectionPool = Pool[Record]
    type RedisConnection = Redis[str]
else:
    type DatabaseConnectionPool = Pool
    type RedisConnection = Redis


class Container:
    _db_pool: ClassVar[DatabaseConnectionPool]
    _redis_pool: ClassVar[ConnectionPool]
    _bot: ClassVar[Bot]

    _DATABASE_URL: Final[str] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    _REDIS_URL: Final[str] = f"redis://{REDIS_HOST}:{REDIS_PORT}?decode_responses=True"

    _injector: Injector
    _db_con: DatabaseConnection
    _redis_con: RedisConnection

    @classmethod
    async def init(cls: type[Self], bot: Bot) -> None:
        cls._bot = bot
        gotten_pool = await create_pool(cls._DATABASE_URL, record_class=Record)

        if gotten_pool is None:
            logger.error("Cannot connect to postgres.")
            exit(-1)

        cls._db_pool = gotten_pool
        cls._redis_pool = ConnectionPool.from_url(cls._REDIS_URL)  # type: ignore  # noqa: PGH003

    async def __aenter__(self) -> Self:
        await self._build_dependencies()
        return self

    async def __aexit__(self, *_: object) -> None:
        await Container._db_pool.release(self._db_con.connection)
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
        self._redis_con = Redis.from_pool(connection_pool=Container._redis_pool)  # type: ignore  # noqa: PGH003
        self._db_con = DatabaseConnection(await self._db_pool.acquire())

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

        singleton_bind(self._injector.binder, DatabaseConnection, to=self._db_con)
        singleton_bind(self._injector.binder, Redis, to=self._redis_con)
        singleton_bind(self._injector.binder, BotNotifier, BotNotifierImpl)
