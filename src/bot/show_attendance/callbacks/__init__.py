from src.bot.common.router.root_router import RootRouter

from .choose_lesson_to_show_attendance import include_choose_lesson_callback_router

__all__ = [
    "include_show_attendance_callbacks",
]


def include_show_attendance_callbacks(root_router: RootRouter) -> None:
    include_choose_lesson_callback_router(root_router)
