from src.bot.common import RootRouter

from .delete_student import include_delete_user_finite_state_router

__all__ = [
    "include_admin_finite_state_router",
]


def include_admin_finite_state_router(root_router: RootRouter) -> None:
    include_delete_user_finite_state_router(root_router)
