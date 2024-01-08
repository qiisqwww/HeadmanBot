from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from asyncpg.pool import PoolConnectionProxy
from injector import Binder, Injector, singleton
from redis.asyncio import Redis

from src.modules.common.application.schedule_api import ScheduleAPI
from src.modules.common.infrastructure.apis.schedule_api import ScheduleApiImpl
from src.modules.common.infrastructure.database.postgres import get_postgres_pool
from src.modules.common.infrastructure.database.redis import get_redis_pool
from src.modules.edu_info.infrastructure.container import assemble_edu_info_module
from src.modules.student_management.infrastructure.container import (
    assemble_student_management_module,
)

__all__ = [
    "project_container",
]


def singleton_bind(binder: Binder, interface, to) -> None:
    binder.bind(interface, to, singleton)


def assemble_common_dependencies(binder: Binder) -> None:
    singleton_bind(binder, ScheduleAPI, to=ScheduleApiImpl)


def assemble_modules(binder: Binder) -> None:
    assemble_common_dependencies(binder)
    assemble_edu_info_module(binder)
    assemble_student_management_module(binder)


@asynccontextmanager
async def project_container() -> AsyncGenerator[Injector, Any]:
    postgres_pool = await get_postgres_pool()
    redis_pool = get_redis_pool()

    postgres_con = await postgres_pool.acquire()
    redis_con = Redis(connection_pool=redis_pool)

    try:
        injector = Injector(assemble_modules)

        singleton_bind(injector.binder, PoolConnectionProxy, to=postgres_con)
        singleton_bind(injector.binder, Redis, to=redis_con)

        yield injector

    finally:
        await postgres_pool.release(postgres_con)
        await redis_con.close()
