from src.bot.common import RootRouter

from .callbacks import include_profile_callbacks_router
from .command import include_profile_command_router
from .finite_state import include_profile_finite_state_router

__all__ = [
    "include_profile_router",
]


def include_profile_router(root_router: RootRouter) -> None:
    include_profile_command_router(root_router)
    include_profile_callbacks_router(root_router)
    include_profile_finite_state_router(root_router)
