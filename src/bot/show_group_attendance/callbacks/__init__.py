from src.bot.common import RootRouter

from .choose_lesson_to_show_attendance import include_choose_lesson_callback_router

__all__ = [
    "include_show_group_attendance_callback_routers",
]


def include_show_group_attendance_callback_routers(root_router: RootRouter) -> None:
    include_choose_lesson_callback_router(root_router)
