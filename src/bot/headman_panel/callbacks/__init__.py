from src.bot.common import RootRouter

from .choose_lesson_to_show_attendance import include_choose_lesson_callback_router
from .choose_student_to_downgrade_callback import (
    include_choose_student_to_downgrade_router,
)
from .choose_student_to_enhance_callback import include_choose_student_to_enhance_router
from .set_vice_headman_callback import include_set_vice_headman_router
from .show_attendance_callback import include_get_attendance_router
from .unset_vice_headman_callback import include_unset_vice_headman_router

__all__ = [
    "include_headman_panel_callbacks",
]


def include_headman_panel_callbacks(root_router: RootRouter) -> None:
    include_choose_lesson_callback_router(root_router)
    include_get_attendance_router(root_router)
    include_set_vice_headman_router(root_router)
    include_unset_vice_headman_router(root_router)
    include_choose_student_to_enhance_router(root_router)
    include_choose_student_to_downgrade_router(root_router)
