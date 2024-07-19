from src.bot.common import RootRouter

from .profile_update import include_profile_update_router
from .enter_group import include_enter_group_router

__all__ = [
    "include_profile_finite_state_router"
]


def include_profile_finite_state_router(root_router: RootRouter) -> None:
    include_profile_update_router(root_router)
    include_enter_group_router(root_router)
