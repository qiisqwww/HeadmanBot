from src.bot.common.router.root_router import RootRouter

from .callbacks import (
    include_show_today_schedule_callback,
    include_show_tomorrow_schedule_callback,
)
from .command import include_get_schedule_command


def include_show_schedule(root_router: RootRouter) -> None:
    include_get_schedule_command(root_router)
    include_show_tomorrow_schedule_callback(root_router)
    include_show_today_schedule_callback(root_router)


__all__ = [
    "include_show_schedule",
]
