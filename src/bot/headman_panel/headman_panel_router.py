from src.bot.common.router.root_router import RootRouter

from .callbacks import include_headman_panel_callbacks
from .command import include_group_panel_command_router

__all__ = [
    "include_group_panel_router",
]


def include_group_panel_router(root_router: RootRouter) -> None:
    include_group_panel_command_router(root_router)
    include_headman_panel_callbacks(root_router)
