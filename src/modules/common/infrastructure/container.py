from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, TypeAlias

from asyncpg.pool import PoolConnectionProxy
from injector import Binder, Injector, InstanceProvider, singleton
from redis.asyncio import Redis

from src.modules.attendance.infrastructure.container import assemble_attendance_module
from src.modules.common.application import UnitOfWork
from src.modules.common.infrastructure.database import get_postgres_pool, get_redis_pool
from src.modules.common.infrastructure.uow import UnitOfWorkImpl
from src.modules.edu_info.infrastructure.container import assemble_edu_info_module
from src.modules.student_management.infrastructure.container import assemble_student_management_module
from src.modules.utils.schedule_api.application import ScheduleAPI
from src.modules.utils.schedule_api.infrastructure import ScheduleApiImpl
from src.modules.utils.throttling.application.repositories import ThrottlingRepository
from src.modules.utils.throttling.infrastructure import ThrottlingRepositoryImpl

__all__ = [
    "project_container",
]

ScheduleApiType: TypeAlias = type[ScheduleAPI]


def singleton_bind(binder: Binder, interface, to) -> None:
    binder.bind(interface, to, singleton)


def assemble_common_dependencies(binder: Binder) -> None:
    singleton_bind(binder, ScheduleApiType, to=InstanceProvider(ScheduleApiImpl))
    singleton_bind(binder, UnitOfWork, to=UnitOfWorkImpl)
    singleton_bind(binder, ThrottlingRepository, ThrottlingRepositoryImpl)


def assemble_modules(binder: Binder) -> None:
    assemble_common_dependencies(binder)
    assemble_edu_info_module(binder)
    assemble_student_management_module(binder)
    assemble_attendance_module(binder)


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
