from src.bot.common import RootRouter

from .command import include_change_group_command_router
from .callbacks import include_change_group_callbacks_router
from .finite_state import include_change_group_fsm_router

__all__ = [
    "include_change_group_router"
]


def include_change_group_router(root_router: RootRouter) -> None:
    include_change_group_command_router(root_router)
    include_change_group_callbacks_router(root_router)
    include_change_group_fsm_router(root_router)
