from src.bot.common.router.root_router import RootRouter

from .callbacks import (
    include_show_schedule_day_callback_router,
    include_show_schedule_week_callback_router
)
from .command import include_get_schedule_command


def include_show_schedule(root_router: RootRouter) -> None:
    include_get_schedule_command(root_router)
    include_show_schedule_day_callback_router(root_router)
    include_show_schedule_week_callback_router(root_router)


__all__ = [
    "include_show_schedule",
]
