from src.kernel import Router

from .callbacks import *
from .commands import *
from .finite_state import registration_finite_state_router

root_router = Router(throttling=True)
root_router.include_routers(
    choose_role_router,
    access_callback_router,
    choose_university_router,
    choose_lesson_callback_router,
    update_attendance_router,
    start_command_router,
    help_router,
    commands_router,
    registration_finite_state_router
)

__all__ = [
    "root_router",
]
