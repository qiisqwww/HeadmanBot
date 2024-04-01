from src.bot.common.router import RootRouter

from .callbacks import include_show_attendance_callbacks
from .command import include_get_attendance_router

__all__ = [
    "include_show_attendance_router",
]


def include_show_attendance_router(root_router: RootRouter) -> None:
    include_show_attendance_callbacks(root_router)
    include_get_attendance_router(root_router)
