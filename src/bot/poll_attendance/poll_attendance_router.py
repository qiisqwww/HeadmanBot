from src.bot.common import RootRouter

from .callbacks import include_poll_attendance_callbacks_router

__all__ = [
    "include_poll_attendance_router",
]


def include_poll_attendance_router(root_router: RootRouter) -> None:
    include_poll_attendance_callbacks_router(root_router)
