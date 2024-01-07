from aiogram import Router as AiogramRouter

from src.modules.student_management.domain import Role

from .middlewares import (
    HandleExceptionMiddleware,
    InjectContextMiddleware,
    InjectDIContainerMiddleware,
    InjectServicesMiddleware,
    InjectStudentMiddleware,
    PermissionManagerMiddleware,
    ThrottlingMiddleware,
)

__all__ = [
    "Router",
]


class Router(AiogramRouter):
    _user_throttling: bool

    def __init__(
        self,
        *,
        must_be_registered: bool | None = None,
        name: str | None = None,
        throttling: bool = False,
        minimum_role: Role | None = None,
    ) -> None:
        super().__init__(name=name)

        if throttling and self.parent_router is not None:
            if isinstance(self.parent_router, AiogramRouter):
                raise TypeError("Router cannot be children of AiogramRouter.")

            if self.parent_router._user_throttling:
                raise ValueError(
                    "Parent router already using throttling, please set 'throttling=False' or"
                    "don't use throttling in parent router."
                )

        self._inject_handle_exception_middleware()
        self._inject_di_container_middleware()

        if throttling:
            self._inject_throttling_middleware()

        self._inject_services_middleware()

        if must_be_registered is not None:
            self._inject_user_middleware(must_be_registered)

        self._inject_context_middleware()

        if minimum_role is not None:
            self._inject_permission_manager_middleware(minimum_role)

    def _inject_user_middleware(self, must_be_registered: bool) -> None:
        self.message.middleware(InjectStudentMiddleware(must_be_registered))
        self.callback_query.middleware(InjectStudentMiddleware(must_be_registered))

    def _inject_permission_manager_middleware(self, min_role: Role) -> None:
        self.message.middleware(PermissionManagerMiddleware(min_role))
        self.callback_query.middleware(PermissionManagerMiddleware(min_role))

    def _inject_throttling_middleware(self) -> None:
        self.message.middleware(ThrottlingMiddleware())
        self.callback_query.middleware(ThrottlingMiddleware())

    def _inject_services_middleware(self) -> None:
        self.message.middleware(InjectServicesMiddleware())
        self.callback_query.middleware(InjectServicesMiddleware())

    def _inject_di_container_middleware(self) -> None:
        self.message.middleware(InjectDIContainerMiddleware())
        self.callback_query.middleware(InjectDIContainerMiddleware())

    def _inject_context_middleware(self) -> None:
        self.message.middleware(InjectContextMiddleware())
        self.callback_query.middleware(InjectContextMiddleware())

    def _inject_handle_exception_middleware(self) -> None:
        self.message.middleware(HandleExceptionMiddleware())
        self.callback_query.middleware(HandleExceptionMiddleware())
