from src.bot.common import RootRouter

from .admin_panel_options_callback import include_admin_panel_options_router
from .delete_student_choice_callback import include_delete_student_choice_router
from .cancel_action_callback import include_cancel_action_router

__all__ = [
    "include_admin_callbacks_router"
]


def include_admin_callbacks_router(root_router: RootRouter) -> None:
    include_admin_panel_options_router(root_router)
    include_delete_student_choice_router(root_router)
    include_cancel_action_router(root_router)
