from aiogram import Dispatcher
from aiogram import Router as AiogramRouter

from .root_middlewares import (
    CheckMessageExpireMiddleware,
    HandleExceptionMiddleware,
    InjectDependenciesMiddleware,
    ThrottlingMiddleware,
)

__all__ = [
    "RootRouter",
]


class RootRouter(AiogramRouter):
    def __init__(self, throttling: bool, name: str | None = None) -> None:
        super().__init__(name=name)

        if self.parent_router is not None and not isinstance(
                self.parent_router,
                (Dispatcher),
        ):
            msg = "Only Dispatcher can be parent for RootRouter."
            raise RuntimeError(msg)

        self._add_handle_exception_middleware()
        self._add_check_message_expire_middleware()

        self._add_inject_container_middleware()

        if throttling:
            self._add_throttling_middleware()

        self._add_inject_dependencies_middleware()

    def _add_handle_exception_middleware(self) -> None:
        self.message.middleware(HandleExceptionMiddleware())
        self.callback_query.middleware(HandleExceptionMiddleware())

    def _add_inject_dependencies_middleware(self) -> None:
        self.message.middleware(InjectDependenciesMiddleware())
        self.callback_query.middleware(InjectDependenciesMiddleware())

    def _add_throttling_middleware(self) -> None:
        self.message.middleware(ThrottlingMiddleware())
        self.callback_query.middleware(ThrottlingMiddleware())

    def _add_check_message_expire_middleware(self) -> None:
        self.callback_query.middleware(CheckMessageExpireMiddleware())
