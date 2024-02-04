from src.bot.common import RootRouter

from .callbacks import include_poll_attendance_callback_routers

__all__ = [
    "include_poll_attendance_routers",
]

def include_poll_attendance_routers(root_router: RootRouter) -> None:
    include_poll_attendance_callback_routers(root_router)
