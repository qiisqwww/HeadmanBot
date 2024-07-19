from src.bot.common import RootRouter

from .show_schedule_certain_date import include_show_schedule_certain_date_router

__all__ = [
    "include_show_schedule_finite_state_router"
]


def include_show_schedule_finite_state_router(root_router: RootRouter) -> None:
    include_show_schedule_certain_date_router(root_router)

