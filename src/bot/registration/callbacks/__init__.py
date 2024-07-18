from src.bot.common.router import RootRouter

from .accept_registration_request_callback import include_accept_registration_callback_router
from .ask_new_fullname_validity_callback import include_ask_new_fullname_validity_router
from .choose_role_callback import include_choose_role_router
from .choose_university_callback import include_choose_university_router

__all__ = [
    "include_registration_callbacks_router",
]


def include_registration_callbacks_router(root_router: RootRouter) -> None:
    include_choose_role_router(root_router)
    include_choose_university_router(root_router)
    include_ask_new_fullname_validity_router(root_router)
    include_accept_registration_callback_router(root_router)
