from src.commands import help_command_router
from src.kernel import Router

from .callbacks import (
    access_callback_router,
    ask_new_fullname_validity_router,
    ask_updated_fullname_validity_router,
    choose_lesson_callback_router,
    choose_role_router,
    choose_university_router,
    profile_menu_router,
    update_attendance_router,
)
from .commands import (
    get_stat_command_router,
    help_router,
    profile_router,
    restart_command_router,
    start_command_router,
)
from .finite_state import profile_update_router, registration_finite_state_router

    ask_fullname_validity_router,
    choose_role_router,
    choose_university_router,
)
from .commands import restart_command_router, start_command_router
from .finite_state import registration_finite_state_router

__all__ = [
    "root_router",
]

root_router = Router(throttling=True)
root_router.include_routers(
    restart_command_router,
    help_command_router,
    choose_role_router,
    access_callback_router,
    choose_university_router,
    start_command_router,
    help_router,
    profile_router,
    get_stat_command_router,
    registration_finite_state_router,
    ask_updated_fullname_validity_router,
    ask_new_fullname_validity_router,
    profile_menu_router,
    profile_update_router
)
