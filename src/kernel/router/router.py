from typing import Iterable

from aiogram import Router as AiogramRouter

from src.kernel.role import Role

from ..config import KernelConfig
from .middlewares import (
    InjectPostgresMiddleware,
    InjectRedisConnectionMiddleware,
    InjectServices,
    InjectStudentMiddleware,
    ServiceClass,
    ThrottlingMiddleware,
)

__all__ = [
    "Router",
]


class Router(AiogramRouter):
    def __init__(
        self,
        name: str | None = None,
        throttling: bool = False,
        inject_user: bool = False,
        roles: Iterable[Role] | None = None,
        services: dict[str, ServiceClass] | None = None,
    ) -> None:
        super().__init__(name=name)

        self._inject_redis_middleware()

        if throttling:
            self._inject_throttling_middleware()

        self._inject_postgres_middleware()
        self._inject_user(inject_user)

        if services is not None:
            self._inject_services(services)

    def _inject_user(self, inject_user: bool) -> None:
        config = KernelConfig()
        self.message.middleware(InjectStudentMiddleware(inject_user, config.find_student_service))
        self.callback_query.middleware(InjectStudentMiddleware(inject_user, config.find_student_service))

    def _inject_redis_middleware(self) -> None:
        self.message.middleware(InjectRedisConnectionMiddleware())
        self.callback_query.middleware(InjectRedisConnectionMiddleware())

    def _inject_postgres_middleware(self) -> None:
        self.message.middleware(InjectPostgresMiddleware())
        self.callback_query.middleware(InjectPostgresMiddleware())

    def _inject_throttling_middleware(self) -> None:
        self.message.middleware(ThrottlingMiddleware())
        self.callback_query.middleware(ThrottlingMiddleware())

    def _inject_services(self, services: dict[str, ServiceClass]) -> None:
        self.message.middleware(InjectServices(**services))
        self.callback_query.middleware(InjectServices(**services))
