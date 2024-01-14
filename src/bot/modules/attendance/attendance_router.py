from src.bot.common.router import RootRouter

from .callbacks import include_attendance_callbacks
from .command import include_get_attendance_command

__all__ = [
    "include_attendance_router",
]


def include_attendance_router(root_router: RootRouter) -> None:
    include_get_attendance_command(root_router)
    include_attendance_callbacks(root_router)
