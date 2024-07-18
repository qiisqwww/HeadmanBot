from src.bot.common import RootRouter

from .callbacks import include_show_schedule_callbacks_router
from .finite_state import include_show_schedule_finite_state_router
from .command import include_show_schedule_command_router

__all___ = [
    "include_show_schedule_router",
]


def include_show_schedule_router(root_router: RootRouter) -> None:
    include_show_schedule_command_router(root_router)
    include_show_schedule_callbacks_router(root_router)
    include_show_schedule_finite_state_router(root_router)
