from src.bot.common import RootRouter

from .cancel_action_callback import include_cancel_action_router
from .change_group_callback import include_change_group_callback_router
from .get_back_callback import include_get_back_callback_router
from quit_group_callback import include_quit_group_callback_router

__all__ = [
    "include_change_group_callbacks_router"
]


def include_change_group_callbacks_router(root_router: RootRouter) -> None:
    include_cancel_action_router(root_router)
    include_change_group_callback_router(root_router)
    include_get_back_callback_router(root_router)
    include_quit_group_callback_router(root_router)