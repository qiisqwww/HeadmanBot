from .accept_request import access_callback_router
from .ask_new_fullname_validity_callback import ask_new_fullname_validity_router
from .ask_updated_field_validity_callback import ask_updated_fullname_validity_router
from .choose_lesson_to_show_attendance import choose_lesson_callback_router
from .choose_role import choose_role_router
from .choose_university import choose_university_router
from .profile_update_callback import profile_menu_router
from .update_attendance import update_attendance_router

__all__ = [
    "choose_role_router",
    "access_callback_router",
    "choose_university_router",
    "choose_lesson_callback_router",
    "update_attendance_router",
    "ask_new_fullname_validity_router",
    "ask_updated_fullname_validity_router",
    "profile_menu_router",
]
