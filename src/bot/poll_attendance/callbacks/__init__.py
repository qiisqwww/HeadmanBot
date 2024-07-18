from src.bot.common.router import RootRouter

from .update_all_attenance import include_update_all_attendances_router
from .update_attendance import include_update_attendance_router

__all__ = [
    "include_poll_attendance_callbacks_router",
]


def include_poll_attendance_callbacks_router(root_router: RootRouter) -> None:
    include_update_attendance_router(root_router)
    include_update_all_attendances_router(root_router)
