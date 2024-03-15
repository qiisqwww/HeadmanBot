from src.bot.common import RootRouter

from .command import include_admin_panel_command_router
from .callbacks import (
    include_admin_panel_options_router,
    include_delete_student_choice_router
)
from .finite_state import include_delete_user_finite_state_router


__all__ = [
    "include_admin_router"
]


def include_admin_router(root_router: RootRouter) -> None:
    include_admin_panel_command_router(root_router)
    include_admin_panel_options_router(root_router)
    include_delete_student_choice_router(root_router)
    include_delete_user_finite_state_router(root_router)
