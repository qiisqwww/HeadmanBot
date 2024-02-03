from src.bot.common.router import RootRouter

from .callbacks import include_show_group_attendance_callback_routers
from .command import include_get_attendance_command

__all__ = [
    "include_show_group_attendance_routers",
]


def include_show_group_attendance_routers(root_router: RootRouter) -> None:
    include_get_attendance_command(root_router)
    include_show_group_attendance_callback_routers(root_router)
