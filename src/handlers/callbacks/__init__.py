from .choose_role import choose_role_router
from .accept_request import access_callback_router
from .choose_lesson_to_show_attendance import choose_lesson_callback_router
from .choose_university import choose_university_router
from .update_attendance import update_attendance_router

__all__ = [
    "choose_role_router",
    "access_callback_router",
    "choose_university_router",
    "choose_lesson_callback_router",
    "update_attendance_router"
]
