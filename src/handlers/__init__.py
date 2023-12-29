from src.kernel import Router

from .callbacks import (
    access_callback_router,
    ask_new_fullname_validity_router,
    choose_lesson_callback_router,
    choose_role_router,
    choose_university_router,
    update_attendance_router,
    ask_updated_fullname_validity_router
)
from .commands import (
    get_stat_command_router,
    help_router,
    restart_command_router,
    start_command_router,
)
from .finite_state import registration_finite_state_router, edit_profile_router

__all__ = [
    "root_router",
]

root_router = Router(throttling=True)
root_router.include_routers(
    restart_command_router,
    update_attendance_router,
    choose_role_router,
    access_callback_router,
    choose_university_router,
    choose_lesson_callback_router,
    start_command_router,
    help_router,
    get_stat_command_router,
    registration_finite_state_router,
    ask_new_fullname_validity_router,
    edit_profile_router,
    ask_updated_fullname_validity_router
)
