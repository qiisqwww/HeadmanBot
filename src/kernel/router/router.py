from aiogram import Router as AiogramRouter

from src.kernel.role import Role

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
    _use_throttling: bool

    def __init__(
        self,
        name: str | None = None,
        throttling: bool = False,
        must_be_registered: bool | None = None,
        minimum_role: Role | None = None,
        services: dict[str, ServiceClass] | None = None,
    ) -> None:
        super().__init__(name=name)

        if throttling and self.parent_router is not None:
            if isinstance(self.parent_router, AiogramRouter):
                raise TypeError("Router cannot be children of AiogramRouter.")

            if self.parent_router._use_throttling:
                raise ValueError(
                    "Parent router already using throttling, please set 'throttling=False' or"
                    "don't use throttling in parent router."
                )

        if services is not None or throttling:
            self._inject_redis_middleware()

        if throttling:
            self._inject_throttling_middleware()

        if services is not None or must_be_registered is not None:
            self._inject_postgres_middleware()

        if must_be_registered is not None:
            self._inject_user(must_be_registered)

        if services is not None:
            self._inject_services(services)

    def _inject_user(self, must_be_registered: bool) -> None:
        from src.kernel.config.config import FIND_USER_SERVICE

        if FIND_USER_SERVICE is None:
            raise TypeError("Find user service is None.")

        self.message.middleware(InjectStudentMiddleware(must_be_registered, FIND_USER_SERVICE))
        self.callback_query.middleware(InjectStudentMiddleware(must_be_registered, FIND_USER_SERVICE))

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
