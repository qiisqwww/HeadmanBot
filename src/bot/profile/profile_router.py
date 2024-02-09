from src.bot.common import RootRouter

from .callbacks import include_ask_updated_field_validity_router, include_profile_menu_router
from .command import include_profile_command_router
from .finite_state import include_profile_update_router

__all__ = [
    "include_profile_router",
]


def include_profile_router(root_router: RootRouter) -> None:
    include_profile_menu_router(root_router)
    include_profile_command_router(root_router)
    include_profile_update_router(root_router)
    include_ask_updated_field_validity_router(root_router)
