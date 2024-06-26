from src.bot.common.router.root_router import RootRouter

from .callbacks import (
    include_show_schedule_date_callback_router,
    include_show_schedule_week_callback_router,
    include_back_to_week_choice_list_callback_router,
    include_ask_certain_date_schedule_router
)
from .command import include_get_schedule_command
from .finite_state import include_show_schedule_certain_date_router

__all__ = [
    "include_show_schedule",
]


def include_show_schedule(root_router: RootRouter) -> None:
    include_get_schedule_command(root_router)
    include_show_schedule_date_callback_router(root_router)
    include_show_schedule_week_callback_router(root_router)
    include_back_to_week_choice_list_callback_router(root_router)
    include_ask_certain_date_schedule_router(root_router)
    include_show_schedule_certain_date_router(root_router)



