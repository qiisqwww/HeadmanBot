from src.bot.common.router import RootRouter

from .choose_lesson_to_show_attendance import include_choose_lesson_callback_router
from .update_all_attenance import include_update_all_attendances_router
from .update_attendance import include_update_attendance_router

__all__ = [
    "include_attendance_callbacks",
]


def include_attendance_callbacks(root_router: RootRouter) -> None:
    include_choose_lesson_callback_router(root_router)
    include_update_attendance_router(root_router)
    include_update_all_attendances_router(root_router)
