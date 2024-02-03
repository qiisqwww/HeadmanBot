from src.bot.common.router import RootRouter

from .accept_request import include_access_callback_router
from .ask_new_fullname_validity_callback import include_ask_new_fullname_validity_router
from .choose_role import include_choose_role_router
from .choose_university import include_choose_university_router

__all__ = [
    "include_registration_callbacks",
]


def include_registration_callbacks(root_router: RootRouter) -> None:
    include_choose_role_router(root_router)
    include_choose_university_router(root_router)
    include_ask_new_fullname_validity_router(root_router)
    include_access_callback_router(root_router)
