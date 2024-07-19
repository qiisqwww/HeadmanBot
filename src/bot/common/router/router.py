from aiogram import Router as AiogramRouter

from src.modules.student_management.domain import Role

from .middlewares import InjectStudentMiddleware, PermissionManagerMiddleware
from .root_router import RootRouter

__all__ = [
    "Router",
]


class Router(AiogramRouter):
    def __init__(
        self,
        must_be_registered: bool | None = False,
        minimum_role: Role = Role.IS_REGISTERED,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)

        if self.parent_router is not None and not isinstance(self.parent_router, RootRouter):
                raise RuntimeError("Router parent can be only RootRouter.")

        if must_be_registered is not None:
            self._add_inject_student_middleware(must_be_registered)

        if must_be_registered:
            self._add_permission_manager_middleware(minimum_role)

    def _add_inject_student_middleware(self, must_be_registered: bool) -> None:
        self.message.middleware(InjectStudentMiddleware(must_be_registered))
        self.callback_query.middleware(InjectStudentMiddleware(must_be_registered))

    def _add_permission_manager_middleware(self, min_role: Role) -> None:
        self.message.middleware(PermissionManagerMiddleware(min_role))
        self.callback_query.middleware(PermissionManagerMiddleware(min_role))
