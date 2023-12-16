from src.kernel import Router

from .callbacks import *
from .commands import *

root_router = Router(throttling=True)
root_router.include_routers(
    choose_role_router,
    access_callback_router,
    choose_university_router,
    choose_lesson_callback_router,
    update_attendance_router,
    start_command_router,
    help_router,
    commands_router
)

__all__ = [
    "root_router",
]
