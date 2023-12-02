from typing import Protocol, TypeVar

from aiogram import Router

from .middlewares import (
    InjectPostgresMiddleware,
    InjectRedisConnectionMiddleware,
    InjectServices,
    ServiceClass,
    ThrottlingMiddleware,
)

__all__ = [
    "NRouter",
]

PermissionEnum = TypeVar("PermissionEnum", covariant=True)


class PermissionsManagerProtocol(Protocol[PermissionEnum]):
    def check_permission(self) -> PermissionEnum:
        ...


class NRouter(Router):
    def __init__(
        self,
        name: str | None = None,
        throttling: bool = False,
        # permissions_manager: tuple[PermissionsManagerProtocol[PermissionEnum], PermissionEnum] | None = None,
        services: dict[str, ServiceClass] | None = None,
    ) -> None:
        super().__init__(name=name)

        self._inject_redis_middleware()

        if throttling:
            self._inject_throttling_middleware()

        self._inject_postgres_middleware()

        if services is not None:
            self._inject_services(services)

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
