from src.bot.common import RootRouter

from .ask_schedule_certain_day_callback import include_ask_certain_date_schedule_router
from .back_to_week_choice_list_callback import include_back_to_week_choice_list_callback_router
from .show_schedule_date_callback import include_show_schedule_date_callback_router
from .show_schedule_week_callback import include_show_schedule_week_callback_router

__all__ = [
    "include_show_schedule_callbacks_router",
]


def include_show_schedule_callbacks_router(root_router: RootRouter) -> None:
    include_show_schedule_date_callback_router(root_router)
    include_show_schedule_week_callback_router(root_router)
    include_back_to_week_choice_list_callback_router(root_router)
    include_ask_certain_date_schedule_router(root_router)
