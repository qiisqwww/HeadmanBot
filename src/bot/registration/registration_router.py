from src.bot.common.router import RootRouter

from .callbacks import include_registration_callbacks
from .command import include_start_command_router
from .finite_state import include_registration_finite_state_router

__all__ = [
    "include_registration_routers",
]


def include_registration_routers(root_router: RootRouter) -> None:
    include_start_command_router(root_router)
    include_registration_finite_state_router(root_router)
    include_registration_callbacks(root_router)
