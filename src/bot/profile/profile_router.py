from src.bot.common import RootRouter

from .callbacks import (
    include_ask_updated_field_validity_router,
    include_profile_menu_router,
    include_leave_group_callback_router,
    include_ask_user_sure_to_leave_group_router,
    include_enter_group_callback_router,
    include_choose_new_university_router,
    include_choose_new_role_router,
    include_accept_student_enter_group_callback_router  # TODO: создать общие роутеры для callback и тд
)
from .command import include_profile_command_router
from .finite_state import include_profile_update_router, include_enter_group_router

__all__ = [
    "include_profile_router",
]


def include_profile_router(root_router: RootRouter) -> None:
    include_profile_menu_router(root_router)
    include_profile_command_router(root_router)
    include_profile_update_router(root_router)
    include_leave_group_callback_router(root_router)
    include_ask_updated_field_validity_router(root_router)
    include_ask_user_sure_to_leave_group_router(root_router)
    include_enter_group_router(root_router)
    include_enter_group_callback_router(root_router)
    include_choose_new_university_router(root_router),
    include_choose_new_role_router(root_router)
    include_accept_student_enter_group_callback_router(root_router)
