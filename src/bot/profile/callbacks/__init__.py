from src.bot.common import RootRouter

from .accept_student_enter_group_callback import include_accept_student_enter_group_callback_router
from .accept_student_leave_group_callback import include_accept_student_leave_group_callback_router
from .ask_updated_field_validity_callback import include_ask_updated_field_validity_router
from .ask_user_sure_to_leave_group_callback import include_ask_user_sure_to_leave_group_router
from .choose_new_role_callback import include_choose_new_role_router
from .choose_new_uni_callback import include_choose_new_university_router
from .enter_group_callback import include_enter_group_callback_router
from .leave_group_callback import include_leave_group_callback_router
from .profile_update_callback import include_profile_menu_router

__all__ = [
    "include_profile_callbacks_router",
]


def include_profile_callbacks_router(root_router: RootRouter) -> None:
    include_profile_menu_router(root_router)
    include_ask_updated_field_validity_router(root_router)
    include_leave_group_callback_router(root_router)
    include_ask_user_sure_to_leave_group_router(root_router)
    include_enter_group_callback_router(root_router)
    include_choose_new_university_router(root_router)
    include_choose_new_role_router(root_router)
    include_accept_student_enter_group_callback_router(root_router)
    include_accept_student_leave_group_callback_router(root_router)
