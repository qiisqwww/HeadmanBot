from src.bot.common import RootRouter

from .callbacks import include_admin_callbacks_router
from .command import include_admin_panel_command_router
from .finite_state import include_admin_finite_state_router

__all__ = [
    "include_admin_router",
]


def include_admin_router(root_router: RootRouter) -> None:
    include_admin_panel_command_router(root_router)
    include_admin_callbacks_router(root_router)
    include_admin_finite_state_router(root_router)
